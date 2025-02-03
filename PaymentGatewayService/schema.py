import graphene
import PaymentGateway.schema


class Query(PaymentGateway.schema.PaymentGatewayQueries, graphene.ObjectType):
    pass


class Mutation(PaymentGateway.schema.PaymentGatewayOperation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)