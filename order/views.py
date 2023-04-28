from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer, MyOrderSerializer
from django.db.models.functions import TruncHour
from django.db.models import Sum


@api_view(['POST'])
# @authentication_classes([authentication.TokenAuthentication])
# @permission_classes([permissions.IsAuthenticated])
def checkout(request):
    user = request.user if request.user.is_authenticated else None #for non authenticated_users
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        print('проверка пройдена')
        # paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])
        paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])
        try:
            serializer.save(user=user, paid_amount=paid_amount)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyOrdersList(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)
    
class AdminOrderList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    def get(self, request, format=None):
        orders = Order.objects.all()
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)


class AdminOrderListDelete(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = MyOrderSerializer(order)
        return Response(serializer.data)
    
    def delete(self, request, pk, format=None):
        order = Order.objects.get(pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    def put(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = MyOrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderChartView(APIView):
    # permission_classes = [permissions.IsAdminUser]
    def get(self, request, *args, **kwargs):
        orders = Order.objects.annotate(
            date_hour=TruncHour('created_at')
        ).values(
            'date_hour'
        ).annotate(
            total=Sum('paid_amount')
        )
        data = []
        for order in orders:
            date = order['date_hour'].strftime('%Y-%m-%d %H:%M:%S')
            value = order['total']
            data.append({'date': date, 'value': value})
        return Response(data)