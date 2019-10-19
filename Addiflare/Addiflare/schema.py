import graphene
import users.schema
import graphql_jwt
from rx import Observable
#import Addicore.schema

class Query(users.schema.Query, graphene.ObjectType):
    pass


class Mutation(users.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

# class Subscription(Addicore.schema.Subscriptions, graphene.ObjectType):
#     class Meta:
#         description = 'The project root subscription definition'

class Subscription(graphene.ObjectType):
    
    count_seconds = graphene.Int(up_to=graphene.Int())


    def resolve_count_seconds(
        root, 
        info, 
        up_to=5
    ):
        return Observable.interval(1000)\
                         .map(lambda i: "{0}".format(i))\
                         .take_while(lambda i: int(i) <= up_to)

schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)
