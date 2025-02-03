import graphene
from PaymentGateway.query import PaymentGatewayQueries
from PaymentGateway.mutations import PaymentGatewayOperation


class Query(PaymentGatewayQueries, graphene.ObjectType):
    pass


class Mutation(PaymentGatewayOperation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)