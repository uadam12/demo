from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import BSSBManager, _


# Create your models here.
class User(AbstractUser):
    ACCESS_CODES = (
        (1, 'Applicant'),
        (2, 'Guest User'),
        (3, 'Admin'),
        (4, 'Main Admin')
    )
    username = None
    email = models.EmailField(_('email address'), unique=True)
    access_code = models.PositiveSmallIntegerField(default=1, choices=ACCESS_CODES)
    is_blocked = models.BooleanField(default=False)
    has_completed_profile = models.BooleanField(default=False)
    paid_registration_fee = models.BooleanField(default=False)
    
    picture = models.ImageField(
        default='/default-user.svg', 
        upload_to='profiles'
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = BSSBManager()
    
    @property
    def dashboard(self):
        return 'applicant:dashboard' if self.access_code < 2 else 'official:dashboard'

    @classmethod
    def admins(cls):
        return cls.objects.filter(access_code=3)
    
    @classmethod
    def guests(cls):
        return cls.objects.filter(access_code=2)
 
    @classmethod
    def applicants(cls):
        return cls.objects.filter(access_code=1)
    
    @classmethod
    def blocked_users(cls):
        return cls.objects.filter(is_blocked=True)

    @classmethod
    def unblocked_users(cls):
        return cls.objects.filter(is_blocked=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"