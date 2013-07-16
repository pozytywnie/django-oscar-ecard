# -*- coding: utf-8 -*-
import hashlib
import json
import logging

from django.conf import settings
from django.db.models import get_model
from django.http import HttpResponse
from django.views import generic

from oscar_ecard import forms
from oscar_ecard import models

logger = logging.getLogger(__name__)


class PaymentRedirectForm(generic.FormView):
    form_class = forms.eCardPaymentForm
    template_name = 'ecard/payment_redirect_form.html'

    def get_form_kwargs(self):
        kwargs = super(PaymentRedirectForm, self).get_form_kwargs()
        order = get_model('order', 'Order').objects.get(id=self.kwargs['order_id'])
        kwargs['initial'].update({'ORDERNUMBER': str(order.id),
                                  'AMOUNT': str(self._get_penny_amount(order.total_incl_tax)),
                                  'NAME': order.user.first_name or 'Klient',
                                  'SURNAME': order.user.last_name or 'Audioapp'})
        hash = self._get_hash(kwargs['initial'])
        kwargs['initial'].update({'HASH': hash})
        return kwargs

    def _get_penny_amount(self, decimal_amount):
        return int(decimal_amount*100)

    def _get_hash(self, form_kwargs):
        fields = forms.eCardPaymentForm().fields
        h = hashlib.new('sha1')
        h.update(fields['MERCHANTID'].initial)
        h.update(form_kwargs['ORDERNUMBER'])
        h.update(form_kwargs['AMOUNT'])
        h.update(fields['CURRENCY'].initial)
        h.update(fields['ORDERDESCRIPTION'].initial.encode('utf-8'))
        h.update(form_kwargs['NAME'].encode('utf-8'))
        h.update(form_kwargs['SURNAME'].encode('utf-8'))
        h.update(fields['AUTODEPOSIT'].initial)
        h.update(fields['PAYMENTTYPE'].initial)
        h.update(fields['LINKFAIL'].initial)
        h.update(fields['LINKOK'].initial)
        h.update(settings.ECARD_PASSWORD)
        return h.hexdigest()


class eCardResponseView(generic.View):
    def post(self, request):
        if 'ORDERNUMBER' in request.POST:
            self._process_ecard_response(request.POST)
        return HttpResponse('OK')

    def _process_ecard_response(self, post):
        try:
            request = models.eCardPaymentRequest.objects.get(order__id=post['ORDERNUMBER'])
        except models.eCardPaymentRequest.DoesNotExist as e:
            logger.exception(e, extra=post)
        else:
            self.status = post['CURRENTSTATE']
            self._validate_response(post)
            body = json.dumps(post)

            models.eCardPaymentResponse.objects.create(body=body, source=request,
                                                       status=self.status,
                                                       amount=request.order.total_incl_tax,
                                                       ip=get_ip(self.request))

    def _validate_response(self, post):
        if post['MERCHANTNUMBER'] != settings.ECARD_MERCHANT_ID:
            logger.error('invalid MERCHANTNUMBER', extra=post)
        if get_ip(self.request) != settings.ECARD_RESPONSE_SERVER_IP:
            self.status = 'FRAUD'
            logger.error('INVALID ECARD_RESPONSE_SERVER_IP', extra=post)


def get_ip(request):
    ip = request.META.get('REMOTE_ADDR', '')
    if settings.USE_X_FORWARDED_HOST and 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META.get('HTTP_X_FORWARDED_FOR', '')
    elif ip == '127.0.0.1' and 'HTTP_X_REAL_IP' in request.META:
        ip = request.META.get('HTTP_X_REAL_IP', '')
    return ip
