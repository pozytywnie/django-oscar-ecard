# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.dispatch import receiver
from django.template import Context
from django.template.loader import get_template
from oscar.apps.customer.models import Email
from oscar.apps.order.models import Order


Transaction = models.get_model('payment', 'Transaction')
Source = models.get_model('payment', 'Source')


class eCardPaymentRequest(Source):
    def is_payed(self):
        return eCardPaymentResponse.objects.filter(source=self, status__in=self.payed_statuses()).exists()

    def payed_statuses(self):
        return ['transfer_accepted', 'transfer_closed', 'payment_deposited', 'payment_closed']


class eCardPaymentResponse(Transaction):
    body = models.TextField()
    ip = models.CharField(max_length=20)


@receiver(models.signals.post_save, sender=eCardPaymentResponse)
def update_order_status(sender, instance, created, **kwargs):
    source = instance.source
    if source.is_payed() and not source.amount_debited:
        source.amount_debited = source.amount_allocated
        source.save()
        order = source.order
        order.status = 'payed'
        order.save()


@receiver(models.signals.post_save, sender=Order)
def send_post_payment_email(sender, instance, **kwargs):
    if instance.status == 'payed':
        mailer = PaymentFinalMailer(instance)
        mailer.send()


class PaymentFinalMailer(object):
    subject_template = 'order/email/payment_final_subject.html'
    text_template = 'order/email/payment_final_text_body.html'
    html_template = 'order/email/payment_final_html_body.html'

    def __init__(self, order):
        self.order = order

    def send(self):
        subject = self._render_template(self.subject_template, {'order': self.order}).strip()
        html_body = self._render_template(self.html_template, {'order': self.order})
        text_body = self._render_template(self.text_template, {'order': self.order})
        instance, created = Email.objects.get_or_create(user=self.order.user, subject=subject, body_text=text_body,
                                                        body_html=html_body)

        if created:
            from_email = 'Audioapp <%s>' % settings.DEFAULT_FROM_EMAIL
            msg = EmailMultiAlternatives(subject, text_body, from_email, [self.order.user.email])
            msg.attach_alternative(html_body, "text/html")
            msg.send()

    def _render_template(self, template, context={}):
        return get_template(template).render(Context(context))
