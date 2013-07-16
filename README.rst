django-oscar-ecard
==================

eCard payments system for django-oscar shop application.


Installation
------------

Package
_______

django-oscar-ecard can be installed as a normal Python package.

Example instalation for pip::

    $ pip install django-facebook-auth


Configuration
-------------

settings.py
___________

Add facebook_auth to INSTALLED_APPS::

    INSTALLED_APPS = (
        ...
        'oscar_ecard',
        ...
    )


To your Shop instance (primary app.py) add the application and urls::

    from oscar_ecard.app import application as ecard_application

    class BaseApplication(Shop):
        ...
        ecard_application = ecard_application
        ...

    def get_urls(self):
        urlpatterns = super(BaseApplication, self).get_urls()
        urlpatterns += patterns(
            '',
            (r'^ecard/', include(self.ecard_application.urls)),
        )
        return urlpatterns


Implement eCardPaymentRequest creation in PaymentDetailsView like so::

    from django.core.urlresolvers import reverse
    from django.db.models import get_model
    from django import http

    from oscar.apps.checkout import views as base_views

    SourceType = get_model('payment', 'SourceType')
    eCardPaymentRequest = get_model('oscar_ecard', 'eCardPaymentRequest')


    class PaymentDetailsView(base_views.PaymentDetailsView):
        def handle_payment(self, order_number, total_incl_tax, **kwargs):
            self._create_source(total_incl_tax)

        def handle_successful_order(self, order):
            super(PaymentDetailsView, self).handle_successful_order(order)
            return http.HttpResponseRedirect(reverse('payment-redirect-form', kwargs={'order_id': order.id}))

        def _create_source(self, total_incl_tax):
            source = eCardPaymentRequest(source_type=self._get_source_type(),
                                         amount_allocated=total_incl_tax)
            self.add_payment_source(source)

        def _get_source_type(self):
            type = SourceType.objects.get(name='eCard')
            return type


In settings set::

    ECARD_RESPONSE_SERVER_IP = '193.178.213.69'
    ECARD_MERCHANT_ID = ''
    ECARD_PASSWORD = ''
    ECARD_SUCCESS_URL = ''
    ECARD_FAIL_URL = ''


In eCard panel at https://pay.ecard.pl/gui/configuration.do set "Adres HTTP powiadomienia POST" as http://yourapp/ecard/post/
