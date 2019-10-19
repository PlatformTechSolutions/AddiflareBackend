"""Addiflare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from graphql_ws.django_channels import GraphQLSubscriptionConsumer
from channels.routing import route_class
from django.contrib import admin
from django.urls import path, include
#from graphene_django_extras.views import ExtraGraphQLView
from graphql.backend import GraphQLCoreBackend
from graphene_django.views import GraphQLView
from django_private_chat import urls as django_private_chat_urls
from django.views.decorators.csrf import csrf_exempt
import Addicore
from . import schema

class GraphQLCustomCoreBackend(GraphQLCoreBackend):
    def __init__(self, executor=None):
        # type: (Optional[Any]) -> None
        super().__init__(executor)
        self.execute_params['allow_subscriptions'] = True


class GraphQLObservableUnboxingView(GraphQLView):
    def execute_graphql_request(
            self, request, data, query, variables, operation_name, show_graphiql=False
    ):
        target_result = None

        def override_target_result(value):
            nonlocal target_result
            target_result = value

        execution_result = super().execute_graphql_request(
            request, data, query, variables, operation_name, show_graphiql)
        if execution_result:
            if isinstance(execution_result, ObservableBase):
                target = execution_result.subscribe(
                    on_next=lambda value: override_target_result(value))
                target.dispose()
            else:
                return execution_result

        return target_result


urlpatterns = [
    path('admin/', admin.site.urls),
    path("graphql/", GraphQLView.as_view(graphiql=True)),
    path("chat/", include(django_private_chat_urls)),
]


channel_routing = [
    route_class(GraphQLSubscriptionConsumer, path=r"^/subscriptions"),
]
