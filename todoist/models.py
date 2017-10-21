# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

#creates tokens for users automatically
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Create your models here.
class auth_user(models.Model):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    def __unicode__(self):
        return self.username

class ToDoList(models.Model):
    user_foreignKey = models.IntegerField(max_length=4, null=True) #ForeignKey(auth_user,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=128)
    CreationDate = models.DateTimeField(default=datetime.now, blank=True)
    def __unicode__(self):
        return self.name

class ToDoItem(models.Model):
    to_do_list_foreignKey = models.ForeignKey(ToDoList,on_delete=models.CASCADE)
    description = models.CharField(max_length=128)
    completed = models.CharField(max_length=128)
    due_date = models.DateField(default=datetime.now, blank=True)
    def __unicode__(self):
        return self.description