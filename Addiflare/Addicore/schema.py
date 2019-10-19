import graphene
from . subscriptions import MessageSubscription
from graphene_django import DjangoObjectType
from .models import Message


# class Subscriptions(graphene.ObjectType):
#     msg = MessageSubscription.Field()

class MessageType(DjangoObjectType):
    class Meta:
        model = Message


