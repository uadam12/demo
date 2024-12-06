from django.db import models
from django.urls import reverse, reverse_lazy

# Create your models here.
class Program(models.Model):
    name = models.CharField(max_length=100, unique=True)
    list_url = reverse_lazy('academic:programs')

    @property
    def update_url(self):
        return reverse('academic:update-program', kwargs={'id':self.pk})
    
    @property
    def delete_url(self):
        return reverse('academic:delete-program', kwargs={'id':self.pk})

    class Meta:
        verbose_name = "program"
        verbose_name_plural = "programs"
        ordering = ("name", )

    def __str__(self):
        return self.name
    
class Level(models.Model):
    name = models.CharField(max_length=100)
    code = models.PositiveIntegerField()
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='levels')
    list_url = reverse_lazy('academic:levels')

    @property
    def update_url(self):
        return reverse('academic:update-level', kwargs={'id':self.pk})
    
    @property
    def delete_url(self):
        return reverse('academic:delete-level', kwargs={'id':self.pk})

    class Meta:
        verbose_name = "level"
        verbose_name_plural = "levels"
        ordering = ("code", "name")
        constraints = [
            models.UniqueConstraint(
                fields=['program', 'code'], 
                name='unique_level_code_per_program'
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.program.name}"


class Course(models.Model):
    title = models.CharField(max_length=255)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='courses')
    list_url = reverse_lazy('academic:courses')

    @property
    def update_url(self):
        return reverse('academic:update-course', kwargs={'id':self.pk})
    
    @property
    def delete_url(self):
        return reverse('academic:delete-course', kwargs={'id':self.pk})

    class Meta:
        verbose_name = "course"
        verbose_name_plural = "courses"
        ordering = ("title", )
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'program'],
                name='unique_course_per_program',
            )
        ]

    def __str__(self):
        return self.title

class InstitutionType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    list_url = reverse_lazy('academic:institution-types')

    @property
    def update_url(self):
        return reverse('academic:update-institution-type', kwargs={'id':self.pk})
    
    @property
    def delete_url(self):
        return reverse('academic:delete-institution-type', kwargs={'id':self.pk})
    
    class Meta:
        verbose_name = "institution_type"
        verbose_name_plural = "institution_types"
        ordering = ("name", )

    def __str__(self):
        return self.name

class Institution(models.Model):
    name = models.CharField(max_length=255)
    institution_type = models.ForeignKey(
        InstitutionType, 
        on_delete=models.CASCADE, 
        related_name='institutions'
    )
    list_url = reverse_lazy('academic:institutions')

    @property
    def update_url(self):
        return reverse('academic:update-institution', kwargs={'id':self.pk})
    
    @property
    def delete_url(self):
        return reverse('academic:delete-institution', kwargs={'id':self.pk})
 
    class Meta:
        verbose_name = "institution"
        verbose_name_plural = "institutions"
        ordering = ("name", )
        
    def __str__(self):
        return self.name