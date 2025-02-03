import graphene
from PaymentGateway.models import PaymentGateway, PaymentTransaction
from graphene_django import DjangoObjectType


class PaymentGatewayType(DjangoObjectType):
    class Meta:
        model = PaymentGateway
        fields = '__all__'


class PaymentTransactionType(DjangoObjectType):
    class Meta:
        model = PaymentTransaction
        fields = '__all__'


class PaymentGatewayQueries(graphene.ObjectType):
    # Query to retrieve all PaymentGateway records.
    get_all_gateways = graphene.List(PaymentGatewayType)

    # Query to retrieve a PaymentGateway record by its gateway_name.
    get_gateway_by_name = graphene.Field(
        PaymentGatewayType,
        gateway_name=graphene.String(required=True)
    )

    def resolve_get_all_gateways(self, info):
        # TODO: Implement logic to retrieve and return all PaymentGateway records.
        pass

    def resolve_get_gateway_by_name(self, info, gateway_name):
        # TODO: Implement logic to retrieve and return a PaymentGateway record based on the provided gateway_name.
        pass
