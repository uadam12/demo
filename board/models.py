from django.db import models
from django.urls import reverse_lazy, reverse
from django.core.validators import RegexValidator

default_motto = 'Supporting Education, Inspiring Excellence'
default_about = [
    "The State Scholarship Board is an essential governmental body dedicated to promoting higher education and ensuring that financial barriers do not hinder talented students from pursuing their academic goals. Established in [Year], the Board offers a variety of merit-based, need-based, and special-purpose scholarships to eligible students within the state. Its mission is to identify and support individuals with exceptional potential who demonstrate academic excellence, community involvement, and leadership skills.",
    "The Board administers scholarships for undergraduate and graduate programs in fields such as science, engineering, arts, business, and education. In addition to academic achievements, the scholarship selection process takes into consideration extracurricular activities, volunteer work, and personal statements.",
    "Each year, thousands of students benefit from the scholarship opportunities provided by the Board, allowing them to access higher education without the burden of overwhelming debt. The State Scholarship Board also partners with local schools, universities, and other educational institutions to raise awareness about the scholarships and assist students in navigating the application process.",
    "For students seeking to apply for financial assistance, the State Scholarship Board offers comprehensive resources, including application guidelines, deadlines, and tips for creating a competitive scholarship portfolio. Students can access the Board’s website to find detailed information on available scholarships, eligibility criteria, and the application process.",
    "By supporting educational opportunities, the State Scholarship Board plays a crucial role in shaping the future workforce and fostering a thriving, educated community.",
]


# Create your models here.
class Board(models.Model):
    motto = models.CharField(max_length=100, default=default_motto)
    registration_is_open = models.BooleanField(default=True)
    new_applicant_can_apply = models.BooleanField(default=True)
    registration_criteria = models.TextField(null=True, blank=True)
    about = models.TextField(default='\n'.join(default_about))
    registration_fee = models.DecimalField(max_digits=10, default=5000.00, decimal_places=2)
    list_url = reverse_lazy('board:index')

    @property
    def criteria(self) -> list:
        data = self.registration_criteria
        return [] if not data else data.split('\n')
    
    @property
    def abouts(self) -> list:
        data = self.about
        return [] if not data else data.split('\n')

    @property
    def info(self) -> str:
        return self.abouts[0]
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *_, **__): pass
    
    @classmethod
    def load(cls):
        return cls.objects.filter(pk=1).get_or_create()[0]
        
    
    def __call__(self, *_, **__):
        return Board.objects.filter(pk=1).get_or_create()[0]

    def __str__(self) -> str:
        return 'Borno State Scholarship Board'

class RegistrationDocument(models.Model):
    name = models.CharField(max_length=255, unique=True)
    required = models.BooleanField(default=True)
    list_url = reverse_lazy('board:reg-documents')
    
    @property
    def update_url(self):
        return reverse('board:update-reg-document', kwargs={'id':self.pk})
    
    @property
    def delete_url(self):
        return reverse('board:delete-reg-document', kwargs={'id':self.pk})
    
    def __str__(self) -> str:
        return self.name

class Bank(models.Model):
    name = models.CharField(max_length=70, unique=True)
    code = models.CharField(max_length=4, primary_key=True, validators=[
        RegexValidator('^\\d{3}$', message='Bank code must be exactly 3 digits.')
    ])
    is_available = models.BooleanField(default=False)
    list_url = reverse_lazy('board:banks')
    
    @property
    def url(self):
        return reverse('board:bank', kwargs={'code':self.pk})

    @property
    def update_url(self):
        return reverse('board:update-bank', kwargs={'code':self.pk})
    
    @property
    def delete_url(self):
        return reverse('board:delete-bank', kwargs={'code':self.pk})

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ('name', )


class LGA(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=70, unique=True)
    list_url = reverse_lazy('board:lgas')
    
    @property
    def url(self):
        return reverse('board:lga', kwargs={'code':self.pk})

    @property
    def update_url(self):
        return reverse('board:update-lga', kwargs={'code':self.pk})
    
    @property
    def delete_url(self):
        return reverse('board:delete-lga', kwargs={'code':self.pk})

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ('name', )