from django.contrib import admin
from .models import Criterion, Requirement, LGA, Bank

# Register your models here.
admin.site.register(Criterion)
admin.site.register(Requirement)
admin.site.register(LGA)
admin.site.register(Bank)
