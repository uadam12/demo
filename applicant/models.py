from django.db import models
from django.core.validators import RegexValidator
from app.validators import validate_phone_number
from users.models import User
from board.models import LGA, Bank
from payment.models import Payment
from academic.models import InstitutionType, Institution, Program, Level, CourseType, Course

# Create your models here.
class PersonalInformation(models.Model):
    GENDER = (
        ('', 'Select your gender'),
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='personal_info')
    guardian_name = models.CharField(max_length=50, null=True)
    guardian_phone_number = models.CharField(max_length=15, default='+234', validators=[validate_phone_number])
    phone_number = models.CharField(max_length=15, unique=True, validators=[validate_phone_number])
    gender = models.CharField(max_length=10, choices=GENDER)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=100)
    bvn = models.CharField(max_length=11, unique=True, validators=[
        RegexValidator('^\\d{11}$', message='BVN must be exactly 11 digits.')
    ])
    nin = models.CharField(max_length=11, unique=True, validators=[
        RegexValidator('^\\d{11}$', message='NIN must be exactly 11 digits.')
    ])
    local_government_area = models.ForeignKey(LGA, on_delete=models.CASCADE, related_name='candidates')
    residential_address = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ('date_of_birth', )
        
    def __str__(self):
        return f"Personal Informtion of {self.user}"

class AcademicInformation(models.Model):
    institution_type = models.ForeignKey(InstitutionType, on_delete=models.CASCADE, related_name='academic_info')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='academic_info')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='academic_info')
    course_type = models.ForeignKey(CourseType, on_delete=models.CASCADE, related_name='academic_info')
    course_of_study = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='academic_info')
    year_of_admission = models.PositiveSmallIntegerField(default=2020)
    year_of_graduation = models.PositiveSmallIntegerField(default=2025)
    id_number = models.CharField(max_length=20)
    current_level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='academic_info')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='academic_info')

    class Meta:
        ordering = ('id_number', )

    
    def __str__(self):
        return f"Academic Informtion of {self.user}"
    
class AccountBank(models.Model):
    account_name = models.CharField(max_length=80)
    account_number = models.CharField(max_length=10, unique=True, validators=[
        RegexValidator('^[0-9]{10}$', message='Account number must be exactly 10 digits.')
    ])
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='account_banks')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account_bank')

    def __str__(self):
        return f"Bank Account details of {self.user}"

class SchoolAttended(models.Model):
    school_name = models.CharField(max_length=50)
    certificate_obtained = models.CharField(max_length=80)
    year_from = models.PositiveSmallIntegerField(default=2020)
    year_to = models.PositiveSmallIntegerField(default=2024)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schools_attended')
    
    @property
    def info(self):
        return (
            self.school_name, self.certificate_obtained,
            str(self.year_from), str(self.year_to)
        )

    
    def __str__(self):
        return f"{self.school_name} | {self.year_from} - {self.year_to}"

class Referee(models.Model):
    fullname = models.CharField(max_length=50)
    occupation = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, validators=[validate_phone_number])
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='referee')

    def __str__(self):
        return f"{self.fullname} | Referee of {self.user}"