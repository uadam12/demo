from django.contrib import admin
from .models import Scholarship, ScholarshipProgram, Application, ApplicationDocument

# Register your models here.
admin.site.register(Scholarship)
admin.site.register(ScholarshipProgram)
admin.site.register(Application)
admin.site.register(ApplicationDocument)
