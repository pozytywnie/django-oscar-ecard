# -*- coding: utf-8 -*-
from django.contrib import admin
from oscar.apps.payment.admin import SourceAdmin

from oscar_ecard import models


class ResponseAdmin(admin.ModelAdmin):
    def order(instance):
        return u'zamówienie #%d dla %s' % (instance.source.order.id, instance.source.order.user.get_full_name())

    list_display = ['source', order, 'status', 'ip']
    list_filter = ['status']


admin.site.register(models.eCardPaymentRequest, SourceAdmin)
admin.site.register(models.eCardPaymentResponse, ResponseAdmin)
