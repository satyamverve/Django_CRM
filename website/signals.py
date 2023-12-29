# signals.py
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

@receiver(post_save, sender=get_user_model())
def AddUserGroup(sender, instance, created, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name='Editor')
        instance.groups.add(group)
