from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    posted_on = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()
    submitted_on = models.DateTimeField(auto_now_add=True)

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    testimonial = models.TextField()
    date = models.DateField()

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

class NewsletterSignup(models.Model):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
