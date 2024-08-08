from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'student'),
        (2, 'tutor'),
        (3, 'admin'),
    )
    
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
    name = models.CharField(max_length=100, blank=False, default='')
    surname = models.CharField(max_length=100, blank=False, default='')

    def is_student(self):
        return self.user_type == 1

    def is_tutor(self):
        return self.user_type == 2

    def is_admin_user(self):
        return self.user_type == 3 or self.is_superuser
