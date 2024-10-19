from django.db import models
from django.core.exceptions import ValidationError
from board.models import Criterion, Requirement
from users.models import User

# Create your models here.
class Registration(models.Model):
    fee = models.DecimalField(
        verbose_name='Registration FEE',
        decimal_places=2, 
        max_digits=10,
        default=0.00, 
    )
    criteria = models.ManyToManyField(Criterion, related_name='registration')
    requirements = models.ManyToManyField(Requirement, related_name='registration')
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs): pass
    
    @classmethod
    def load(cls):
        instance, _ = cls.objects.filter(pk=1).get_or_create()
        return instance

class Document(models.Model):
    image = models.ImageField(upload_to='registration_documents', null=True, blank=True)
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='registration_documents'
    )

    requirement = models.ForeignKey(
        Requirement, 
        on_delete=models.CASCADE, 
        related_name='registration_documents'
    )
    
    def clean(self) -> None:
        if self.requirement.is_compulsary and not self.image:
            raise ValidationError({
                'image': f"You need to upload your {self.requirement.text}"
            })

        return super().clean()
    
    def __str__(self) -> str:
        return f"{self.requirement.text} of {self.owner}"