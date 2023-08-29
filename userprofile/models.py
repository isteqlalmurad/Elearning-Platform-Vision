from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(verbose_name="Date of Birth")
    likes = models.TextField(null=True, blank=True)
    image = models.ImageField(default='default.pic', upload_to='profile_pics/')

    def __str__(self):
        return self.user.username


# this is the intial model for keeping progress it will certinly be changed later on now just leaving it for fun

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson_completed = models.IntegerField(default=0)
    energyPoints = models.IntegerField(default=0)
    # Areas where the student needs improvement
    weak_points = models.TextField(null=True, blank=True)
    report = models.TextField(null=True, blank=True)  # Generated by GPT-3.5


def __str__(self):
    return f"{self.user.username} - {self.report or 'No report'}"
