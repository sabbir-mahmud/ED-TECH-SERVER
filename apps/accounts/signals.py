# imports
from random import randint

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save

from .models import Profile

# user model
User = get_user_model()

def verifier(user, token):
 subject = 'Learn With Sabbir:: Verify your account'
 msg = f' Hello {user.first_name} {user.last_name} your verify code is {token}'
 from_email = settings.EMAIL_HOST_USER
 recipient_list = [user.email]
 send_mail(subject=subject, message=msg, from_email=from_email,recipient_list=recipient_list)

# profile signals
def create_profile(created, instance,*args, **kwargs):
 code = f'{randint(0,9)}{randint(0,9)}{randint(0,9)}{randint(0,9)}{randint(0,9)}{randint(0,9)}'
 if created:
  Profile.objects.create(
   user=instance,
   name=f'{instance.first_name} {instance.last_name}',
   gender=instance.gender,
   verifying_code= code
  )
  verifier(instance,code)




post_save.connect(create_profile, sender=User)
