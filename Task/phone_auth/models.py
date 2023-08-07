from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    authorization_code = models.CharField(max_length=4)
    invite_code = models.CharField(max_length=6, null=True)
    is_authenticated = models.BooleanField(default=False)


class InviteCode(models.Model):
    code = models.CharField(max_length=6)
    used_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='used_invite_codes')
