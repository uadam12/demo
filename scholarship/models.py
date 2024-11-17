import random, string
from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError
from board.models import Criterion, Requirement, Bank
from academic.models import Program, Institution, Level, Course
from users.models import User



# Create your models here.
class Scholarship(models.Model):
    description = models.TextField()
    title = models.CharField(max_length=150)
    application_commence = models.DateTimeField()
    application_deadline = models.DateTimeField()
    application_fee = models.DecimalField(max_digits=6, decimal_places=2)
    criteria = models.ManyToManyField(Criterion, related_name='public_scholarships')
    requirements = models.ManyToManyField(Requirement, related_name='public_scholarships')
    
    
    def clean(self) -> None:
        if self.application_commence >= self.application_deadline:
            raise ValidationError({
                'application_commence': 'Application commencement date must be before application deadline date.'
            })

        return super().clean()
    
    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    @property
    def application_is_open(self):
        return self.application_commence <= datetime.now() <= self.application_deadline

    def __str__(self) -> str:
        return self.title
    
    @classmethod
    def past_scholarships(cls):
        return cls.objects.filter(application_deadline__lt = datetime.now())
    
    @classmethod
    def upcoming_scholarships(cls):
        return cls.objects.filter(application_commence__gt = datetime.now())
    
    @classmethod
    def open_scholarships(cls):
        return cls.objects.filter(
            application_commence__lt = datetime.now(), 
            application_deadline__gt = datetime.now()
        )

class ScholarshipProgram(models.Model):
    disbursement_amount = models.DecimalField(max_digits=10, decimal_places=2)
    program = models.ForeignKey(
        Program, 
        on_delete=models.CASCADE, 
        related_name='internal_scholarships'
    )
    scholarship = models.ForeignKey(
        Scholarship, 
        on_delete=models.CASCADE, 
        related_name='programs'
    )
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['program', 'scholarship'], name='unique program per scholarship'
            )
        ]
        
    def clean(self, *args, **kwargs):
        program_exists = ScholarshipProgram.objects.filter(
            scholarship_id=self.scholarship_id, 
            program_id=self.program_id
        ).exclude(id=self.id).exists()
        
        if program_exists: raise ValidationError({
            'program': f"{self.program} already exists for {self.scholarship}"
        })
    
        return super().clean(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.program)
    

# Application
class Application(models.Model):
    @property
    def declerations(self):
        return [
            f"I <b><u>{self.applicant.first_name}</u></b> hereby declare that the information provided above is to the best of my knowledge and belief accurate in every details.",
            'If given this scholarship, I will also comply strictly with the Rules and Regulations of the Borno State Scholarship Board.'
        ]

    schools_attended = [
        ('School Name', 'Qualification Obtained', 'From Date', 'To Date'),
        ('Kamsulem Junior Day Secondary School', 'JSCE', '2013', '2015'),
        ('Government Colledge Maiduguri Borno State', 'SSCE', '2016', '2029')
    ]
    
    STATUS = (
        ('Pending', 'Pending'), 
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    DISBURSEMENT_STATUS = (
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid')
    )
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=15, choices=STATUS, default='Pending')
    disbursement_status = models.CharField(max_length=15, choices=DISBURSEMENT_STATUS, default='Unpaid')
    application_id = models.CharField(max_length=20)
    applied_on = models.DateTimeField(auto_now_add=True)
    
    instituion = models.ForeignKey(Institution, on_delete=models.RESTRICT, related_name='applications')
    program = models.ForeignKey(Program, on_delete=models.RESTRICT, related_name='applications')
    course_of_study = models.ForeignKey(Course, on_delete=models.RESTRICT, related_name='applications')
    level = models.ForeignKey(Level, on_delete=models.RESTRICT, related_name='applications')
    id_number = models.CharField(max_length=50)
    admission_year = models.CharField(max_length=4)
    graduation_year = models.CharField(max_length=4)

    account_bank = models.ForeignKey(Bank, on_delete=models.RESTRICT, related_name='applications')
    account_name = models.CharField(max_length=50)
    account_number = models.CharField(max_length=10)
    
    referee_name = models.CharField(max_length=50)
    referee_phone_number = models.CharField(max_length=10)
    referee_occupation = models.CharField(max_length=50)

    @classmethod
    def get_or_create(cls, applicant, scholarship):
        try:
            model = cls.objects.filter(applicant=applicant, scholarship=scholarship).get()
        except cls.DoesNotExist:
            model = cls(applicant=applicant, scholarship=scholarship)
            model.applicant = applicant
            model.scholarship = scholarship

            academic = applicant.academic_info
            model.course_of_study = academic.course_of_study
            model.instituion = academic.institution
            model.id_number = academic.id_number
            model.admission_year = academic.year_of_admission
            model.graduation_year = academic.year_of_graduation
            model.level = academic.current_level
            model.program = academic.program
        
            account = applicant.account_bank
            model.account_bank = account.bank
            model.account_name = account.account_name
            model.account_number = account.account_number
        
            referee = applicant.referee
            model.referee_name = referee.fullname
            model.referee_phone_number = referee.phone_number,
            model.referee_occupation = referee.occupation
        
            model.save()
        except:
            model = None

        return model

    def save(self, *args, **kwargs):
        while not self.application_id:
            id = 'BSSB'+''.join(
                random.choices(string.digits, k=16)
            )
            application_with_same_id_exist = Application.objects.filter(application_id=id).exists()

            if not application_with_same_id_exist:
                self.application_id = id
            
        return super().save(*args, **kwargs)
    def __str__(self) -> str:
        return f"Application of {self.applicant} for {self.scholarship}"

class ApplicationDocument(models.Model):
    image = models.ImageField(upload_to='application_documents', null=True, blank=True)
    application = models.ForeignKey(
        Application, 
        on_delete=models.CASCADE, 
        related_name='documents'
    )

    requirement = models.ForeignKey(
        Requirement, 
        on_delete=models.CASCADE, 
        related_name='application_documents'
    )
    
    def clean(self) -> None:
        if self.requirement.is_compulsary and not self.image:
            raise ValidationError(f"You need to upload your {self.requirement.text}")

        return super().clean()
    
    def __str__(self) -> str:
        return f"{self.requirement.text} of {self.application.applicant}"