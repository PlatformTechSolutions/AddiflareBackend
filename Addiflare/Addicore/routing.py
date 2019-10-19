# app/routing.py
from graphene_django_subscriptions.consumers import GraphqlAPIDemultiplexer
from channels.routing import route_class
from .subscriptions import MessageSubscription


class CustomAppDemultiplexer(GraphqlAPIDemultiplexer):
    consumers = {
        'users': UserSubscription.get_binding().consumer,
    }


app_routing = [
    route_class(CustomAppDemultiplexer)
]
