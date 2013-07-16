from django.conf.urls import patterns
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from oscar.core.application import Application

from oscar_ecard import views


class eCardPaymentApplication(Application):
    payment_redirect_view = views.PaymentRedirectForm
    ecard_response_view = views.eCardResponseView

    def get_urls(self):
        urlpatterns = patterns(
            '',
            url(r'^pay/(?P<order_id>[0-9]+)/$', self.payment_redirect_view.as_view(), name='payment-redirect-form'),
            url(r'^post/$', csrf_exempt(self.ecard_response_view.as_view())),
        )
        return urlpatterns


application = eCardPaymentApplication()
