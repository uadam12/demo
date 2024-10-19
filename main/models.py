from django.db import models


# Create your models here.
class Article(models.Model):
    headline = models.CharField(max_length=100)
    headline_image = models.ImageField(default='/headline.png', upload_to='headline-images')
    content = models.TextField()
    is_public = models.BooleanField(default=True)
    publish_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    @property
    def contents(self):
        res = self.content.split('\n')
        return [i.strip() for i in res]

    def __str__(self) -> str:
        return self.headline
    
    class Meta:
        ordering = ('-publish_on', 'headline')
        
class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    subject = models.CharField(max_length=150)
    body = models.TextField()
    send_on = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.name}: {self.subject}"

    class Meta:
        ordering = ('-send_on', 'subject')