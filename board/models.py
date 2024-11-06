from django.db import models
from django.core.validators import RegexValidator


# Create your models here.
class Criterion(models.Model):
    text = models.CharField(verbose_name='Criterion text', max_length=100)
        
    def __str__(self):
        return self.text

    class Meta:
        ordering = ('text', )
        
class Requirement(models.Model):
    text = models.CharField(verbose_name='Requirement text', max_length=100)
    is_compulsory = models.BooleanField(default=True)

    def __str__(self):
        asterick = '*' if self.is_compulsory else ''

        return asterick + self.text

    class Meta:
        ordering = ('text', )
        constraints = [
            models.UniqueConstraint(fields=['text', 'is_compulsory'], name='Unique-requirement')
        ]

class Bank(models.Model):
    name = models.CharField(max_length=70, unique=True)
    code = models.CharField(max_length=4, primary_key=True, validators=[
        RegexValidator('^\\d{3}$', message='Bank code must be exactly 3 digits.')
    ])
    is_available = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ('name', )


class LGA(models.Model):
    code = models.CharField(max_length=5, null=True, blank=True)
    name = models.CharField(max_length=70, unique=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ('name', )