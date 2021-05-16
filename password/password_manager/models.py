from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class AddAccount(models.Model):
    PASSWORD_CATEGORIES = (
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('gmail', 'Gmail'),
        ('others', 'Others')
    )

    category = models.CharField(max_length=30, choices=PASSWORD_CATEGORIES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    other_account = models.CharField(max_length=30, null=True, blank=True)
    created_on = models.DateTimeField(default=datetime.now)
    user_name = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=100)
    enc_key = models.CharField(max_length=100)

    def __str__(self):
        return f'Account for: {self.category}'

