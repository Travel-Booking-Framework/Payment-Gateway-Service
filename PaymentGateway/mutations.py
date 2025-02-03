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


class PaymentGatewayOperation(graphene.ObjectType):
    # GraphQL field for creating a PaymentGateway record.
    create_payment_gateway = graphene.Field(
        PaymentGatewayType,
        gateway_name=graphene.String(required=True),
        api_url=graphene.String(required=True),
        merchant_id=graphene.String(required=True),
        API_key=graphene.String(required=True),
        active=graphene.Boolean(required=False, default_value=True)
    )

    # GraphQL field for updating a PaymentGateway record.
    update_payment_gateway = graphene.Field(
        PaymentGatewayType,
        id=graphene.ID(required=True),
        gateway_name=graphene.String(),
        api_url=graphene.String(),
        merchant_id=graphene.String(),
        API_key=graphene.String(),
        active=graphene.Boolean()
    )

    def resolve_create_payment_gateway(self, info, gateway_name, api_url, merchant_id, API_key, active):
        # TODO: Implement the logic to create a new PaymentGateway record.
        pass

    def resolve_update_payment_gateway(self, info, id, gateway_name=None, api_url=None, merchant_id=None, API_key=None,
                                       active=None):
        # TODO: Implement the logic to update an existing PaymentGateway record.
        pass
