from django.contrib import admin
from .models import Board, RegistrationDocument, LGA, Bank

# Register your models here.
admin.site.register(Board)
admin.site.register(RegistrationDocument)
admin.site.register(LGA)
admin.site.register(Bank)
