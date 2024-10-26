from django.db import models
from users.models import User
from scholarship.models import Scholarship


# Create your models here.
class Payment(models.Model):
    TYPES = (
        (1, 'Registration FEE'),
        (2, 'Application FEE'),
        (3, 'Disbursement'),
    )
    amount = models.PositiveIntegerField()
    rrr = models.CharField(max_length=20, unique=True)
    code = models.PositiveSmallIntegerField(choices=TYPES, default=1)
    paid_on = models.DateField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    payer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='payments'
    )
    
    @classmethod
    def registration_fees(cls):
        return cls.objects.filter(code=1)
    
    @classmethod
    def application_fees(cls):
        return cls.objects.filter(code=2)

    @classmethod
    def disbursement(cls):
        return cls.objects.filter(code=3)

    def __str__(self) -> str:
        return f"Payment of N{self.amount} by {self.payer}"
    
    class Meta:
        ordering = ('-paid_on', )
        

class ApplicationFEE(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='application_fees')
    payment = models.OneToOneField(
        Payment,
        on_delete=models.SET_DEFAULT,
        default=None,
        related_name='application_fee'
    )
    
    scholarship = models.ForeignKey(
        Scholarship,
        on_delete=models.CASCADE,
        related_name='application_fees'
    )
    
    @property
    def paid(self):
        return self.payment is not None

    def save(self, *args, **kwargs):
        self.payment.code = 2
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Application FEE - {self.payment}"


class Disbursement(models.Model):
    payment = models.OneToOneField(
        Payment,
        on_delete=models.CASCADE,
        related_name='disbursement'
    )
    
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='disbursements'
    )
    
    def save(self, *args, **kwargs):
        self.payment.code = 3
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"Disbursement - {self.payment}"
