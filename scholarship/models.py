import random, string
from datetime import datetime
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from board.models import Bank
from academic.models import Program, Institution, Level, Course
from applicant.models import SchoolAttended
from payment.models import Payment
from users.models import User


# Create your models here.
class Scholarship(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.BooleanField(default=True)
    application_fee = models.DecimalField(max_digits=6, decimal_places=2)
    program = models.ForeignKey(Program, on_delete=models.RESTRICT, related_name='scholarships')
    disbursement_amount = models.DecimalField(max_digits=10, decimal_places=2, default=50_000.00)
    application_commence = models.DateTimeField()
    application_deadline = models.DateTimeField()
    eligibility_criteria = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def applications(self):
        return Application.objects.filter(scholarship=self)
    
    @property
    def criteria(self):
        criteria:str = self.eligibility_criteria
        return criteria.split('\n') if criteria else []
    
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

class ApplicationDocument(models.Model):
    name = models.CharField(max_length=255)
    required = models.BooleanField(default=True)
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE, related_name='app_documents')

    @property
    def update_url(self):
        return reverse('scholarship:update-app-document', kwargs={'id':self.pk})
    
    @property
    def delete_url(self):
        return reverse('scholarship:delete-app-document', kwargs={'id':self.pk})
    
    def __str__(self) -> str:
        return self.name

class Application(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('incomplete', 'Incomplete'),
    )
    
    application_id = models.CharField(max_length=20)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS, default='incomplete')
    application_fee_payment = models.ForeignKey(Payment,null=True, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
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

    @property
    def url(self):
        return reverse('scholarship:application', kwargs={'application_id':self.application_id})
    
    @property
    def approve_url(self):
        return reverse('scholarship:approve-application', kwargs={'id':self.id})
    
    @property
    def reject_url(self):
        return reverse('scholarship:reject-application', kwargs={'id':self.id})

    @property
    def declerations(self):
        return [
            f"I <b><u>{self.applicant.first_name}</u></b> hereby declare that the information provided above is to the best of my knowledge and belief accurate in every details.",
            'If given this scholarship, I will also comply strictly with the Rules and Regulations of the Borno State Scholarship Board.'
        ]
    
    @property
    def schools_attended(self):
        schools = SchoolAttended.objects.filter(user=self.applicant).order_by('-id')[:5]
        schools = [school.info for school in schools]
        schools.insert(0, ('School Name', 'Qualification Obtained', 'From Date', 'To Date'))

        return schools

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
        return f"Application by {self.applicant} for {self.scholarship.title}"

class Document(models.Model):
    image = models.ImageField(upload_to='application_documents', null=True, blank=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents')
    app_document = models.ForeignKey(ApplicationDocument, on_delete=models.CASCADE, related_name='documents')

    def __str__(self) -> str:
        return f"{self.app_document} of {self.application.applicant}"