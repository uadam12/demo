from django.contrib import admin
from .models import Program, Level, InstitutionType, Institution, CourseType, Course
# Register your models here.


admin.site.register(Program)
admin.site.register(Level)
admin.site.register(InstitutionType)
admin.site.register(Institution)
admin.site.register(CourseType)
admin.site.register(Course)