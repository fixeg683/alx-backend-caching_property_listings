import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from .models import Order, Customer  # Your actual models

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer

class OrderType(DjangoObjectType):
    class Meta:
        model = Order

class Query(graphene.ObjectType):
    total_customers = graphene.Int()
    total_orders = graphene.Int()
    total_revenue = graphene.Decimal()
    
    def resolve_total_customers(self, info):
        return Customer.objects.count()
    
    def resolve_total_orders(self, info):
        return Order.objects.count()
    
    def resolve_total_revenue(self, info):
        return Order.objects.aggregate(total=models.Sum('total_amount'))['total'] or 0

schema = graphene.Schema(query=Query)