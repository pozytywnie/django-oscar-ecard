# -*- coding: utf-8 -*-
from django.conf import settings
from django import forms


class eCardPaymentForm(forms.Form):
    COUNTRY = forms.CharField(widget=forms.HiddenInput, initial="616")
    MERCHANTID = forms.CharField(widget=forms.HiddenInput, initial=settings.ECARD_MERCHANT_ID)
    CURRENCY = forms.CharField(widget=forms.HiddenInput, initial="985")
    LANGUAGE = forms.CharField(widget=forms.HiddenInput, initial="PL")
    AUTODEPOSIT = forms.CharField(widget=forms.HiddenInput, initial="1")
    PAYMENTTYPE = forms.CharField(widget=forms.HiddenInput, initial="ALL")
    TRANSPARENTPAGES = forms.CharField(widget=forms.HiddenInput, initial="1")
    CHARSET = forms.CharField(widget=forms.HiddenInput, initial="UTF-8")
    HASHALGORITHM = forms.CharField(widget=forms.HiddenInput, initial="SHA1")
    ORDERDESCRIPTION = forms.CharField(widget=forms.HiddenInput, initial=u'Audioapp.pl')

    LINKFAIL = forms.CharField(widget=forms.HiddenInput, initial=settings.ECARD_FAIL_URL)
    LINKOK = forms.CharField(widget=forms.HiddenInput, initial=settings.ECARD_SUCCESS_URL)

    ORDERNUMBER = forms.CharField(widget=forms.HiddenInput)
    AMOUNT = forms.CharField(widget=forms.HiddenInput)
    NAME = forms.CharField(widget=forms.HiddenInput)
    SURNAME = forms.CharField(widget=forms.HiddenInput)
    HASH = forms.CharField(widget=forms.HiddenInput)
