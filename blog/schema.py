from django.contrib.auth import get_user_model
from addiCore.models import Blog
import jwt
from django.core.mail import send_mail
from django.conf import settings
import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q

class ProfileType(DjangoObjectType):
    class Meta:
        model= Blog