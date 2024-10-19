from django.db import models

# Create your models here.
class Program(models.Model):
    name = models.CharField(max_length=25, unique=True)
    
    class Meta:
        verbose_name = "program"
        verbose_name_plural = "programs"
        ordering = ("name", )

    def __str__(self):
        return self.name
    
class Level(models.Model):
    name = models.CharField(max_length=20)
    code = models.PositiveIntegerField()
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='levels')

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


class CourseType(models.Model):
    title = models.CharField(max_length=100, unique=True)
    
    def __str__(self) -> str:
        return self.title

class Course(models.Model):
    title = models.CharField(max_length=100, unique=True)
    course_type = models.ForeignKey(CourseType, on_delete=models.CASCADE, related_name='courses')

    class Meta:
        verbose_name = "course"
        verbose_name_plural = "courses"
        ordering = ("title", )

    def __str__(self):
        return self.title

class InstitutionType(models.Model):
    name = models.CharField(max_length=150, unique=True)
    
    class Meta:
        verbose_name = "institution_type"
        verbose_name_plural = "institution_types"
        ordering = ("name", )

    def __str__(self):
        return self.name

class Institution(models.Model):
    name = models.CharField(max_length=150)
    institution_type = models.ForeignKey(
        InstitutionType, 
        on_delete=models.CASCADE, 
        related_name='institutions'
    )
 
    class Meta:
        verbose_name = "institution"
        verbose_name_plural = "institutions"
        ordering = ("name", )
        
    def __str__(self):
        return self.name