import graphene
import grpc
import json
from kafka import KafkaProducer
from PaymentGateway.models import PaymentTransaction
from graphene_django import DjangoObjectType
from generated import payment_callback_pb2, payment_callback_pb2_grpc  # Import gRPC files

# Kafka Configuration
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # Update based on your Kafka setup
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

class PaymentTransactionType(DjangoObjectType):
    class Meta:
        model = PaymentTransaction
        fields = '__all__'


class PaymentGatewayOperation(graphene.ObjectType):
    process_payment = graphene.Field(
        PaymentTransactionType,
        transaction_id=graphene.ID(required=True),
        wallet_uuid=graphene.String(required=True),
        amount=graphene.Float(required=True),
    )

    def resolve_process_payment(self, info, transaction_id, wallet_uuid, amount):
        """
        Simulates a bank payment, then:
        - Calls Wallet Microservice via gRPC
        - Publishes a Kafka event
        """
        try:
            # Simulating bank payment success (replace with actual API call)
            payment_successful = True  

            if payment_successful:
                # Update transaction status in DB
                transaction = PaymentTransaction.objects.get(id=transaction_id)
                transaction.status = "completed"
                transaction.save()

                #  Call Wallet Microservice via gRPC
                self.send_payment_callback(transaction_id, wallet_uuid, amount)

                #  Publish Kafka Event
                event = {
                    "transaction_id": transaction_id,
                    "wallet_uuid": wallet_uuid,
                    "amount": amount,
                    "status": "completed"
                }
                producer.send('payment_wallet', event)
                producer.flush()

                return transaction
            else:
                raise Exception("Payment failed.")

        except Exception as e:
            raise Exception(f"Payment processing failed: {e}")

    def send_payment_callback(self, transaction_id, wallet_uuid, amount):
        """
        Calls Wallet Microservice via gRPC after successful payment.
        """
        try:
            # Connect to Wallet Microservice
            channel = grpc.insecure_channel('wallet_service:50053')  # Update to match your service
            stub = payment_callback_pb2_grpc.PaymentCallbackStub(channel)

            # Send gRPC request
            response = stub.ProcessPaymentCallback(
                payment_callback_pb2.PaymentCallbackRequest(
                    transaction_id=transaction_id,
                    status="completed",
                    transaction_type="credit",
                    amount=amount,
                    wallet_uuid=wallet_uuid
                )
            )

            if response.status != "SUCCESS":
                raise Exception(f"Wallet update failed: {response.message}")

        except Exception as e:
            raise Exception(f"gRPC request failed: {e}")
