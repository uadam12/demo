from django.contrib import admin
from .models import Payment, ApplicationFEE, Disbursement


# Register your models here.
admin.site.register(Payment)
admin.site.register(ApplicationFEE)
admin.site.register(Disbursement)
