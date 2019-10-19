from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100, default="")
    fname = models.CharField(max_length=100, default="")
    lname = models.CharField(max_length=100, default="")
    headerPic = models.CharField(max_length=300,  default="header.png")
    profilePic = models.CharField(max_length=300, default="logo.png")
    city = models.CharField(max_length=100, default="")
    state = models.CharField(max_length=100, default="")
    country = models.CharField(max_length=100, default="")
    occupation = models.CharField(max_length=100, default="")
    shortdescription = models.CharField(max_length=300, default="")
    verified = models.BooleanField(max_length=100, default=False)
    emailverified = models.BooleanField(default=False)
    emailotp = models.CharField(max_length=100, null=True, blank=True)
    is2fa = models.BooleanField(default=False)
    issuspended = models.BooleanField(default=False)
    suspendedtill = models.DateField(blank=True, null=True)
    isPsy = models.BooleanField(default=False)
    ispublic = models.BooleanField(default=True)


class Blog(models.Model):
    author = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="")
    shortDescription = models.TextField()
    content = models.TextField()
    thumbnail = models.FileField()
    image = models.FileField()
    created_at = models.DateTimeField()
    categories = models.CharField(max_length=100)
    isDraft = models.BooleanField()
    isPublished = models.BooleanField()
