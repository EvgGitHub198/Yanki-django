from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
from pytz import timezone
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer, MyOrderSerializer
from django.db.models.functions import TruncHour, TruncDay
from django.db.models import Sum
from datetime import datetime, timedelta
from pandas import pandas as pd
from django.db.models import Sum
from django.http import JsonResponse
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta



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
    permission_classes = [permissions.IsAdminUser]
    def get(self, request, format=None):
        orders = Order.objects.all()
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)



class AdminOrderListDelete(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

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
    

import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from django.db.models import Avg

class MonthSalesForecastView(APIView):

    def get(self, request, *args, **kwargs):
        # Получаем данные продаж за предыдущие месяцы
        start_date = datetime.now() - timedelta(days=120)
        orders = Order.objects.filter(created_at__gte=start_date)
        daily_sales = orders.annotate(date=TruncDay('created_at')).values('date').annotate(total=Sum('paid_amount')).order_by('date')


        last_month = datetime.now() - relativedelta(months=1)
        last_month_orders = Order.objects.filter(created_at__month=last_month.month)
        last_month_sales = last_month_orders.annotate(date=TruncDay('created_at')).values('date').annotate(total=Sum('paid_amount')).order_by('date')
        last_month_average = last_month_sales.aggregate(Avg('total'))['total__avg']
        
        max_sale = int(last_month_average)*0.8
        # Преобразуем данные в формат, который требуется для SARIMAX
        sales = []
        for item in daily_sales:
            sale = item['total']
            # Ограничиваем значение продаж в диапазоне от 0 до avg_sales
            sale = np.clip(sale, 0, max_sale)
            sales.append(sale)

        # Создаем DataFrame и заполняем пропущенные значения средними значениями по столбцу
        df = pd.DataFrame({'sales': sales})
        df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
        df = df.fillna(df.mean())

        p = 1
        d = 1
        q = 1
        P = 1
        D = 1
        Q = 1

        # Создаем модель SARIMAX и обучаем ее на данных продаж
        model = SARIMAX(df, order=(p, d, q), seasonal_order=(P, D, Q, 12))
        model_fit = model.fit(disp=0)

        # Получаем прогноз на следующий месяц
        forecast = model_fit.forecast(steps=30)
        forecast_data = []
        for i, value in enumerate(forecast.tolist()):
            date = (datetime.now() + timedelta(days=i+1)).strftime('%Y-%m-%d')
            forecast_data.append({'date': date, 'value': value})
        
        
        # Возвращаем данные прогноза в формате JSON
        return JsonResponse(forecast_data, safe=False)





import numpy as np

class YearSalesForecastView(APIView):

    def get(self, request, *args, **kwargs):
        # Получаем данные продаж за предыдущие месяцы
        start_date = datetime.now() - timedelta(days=120)
        orders = Order.objects.filter(created_at__gte=start_date)
        daily_sales = orders.annotate(date=TruncDay('created_at')).values('date').annotate(total=Sum('paid_amount')).order_by('date')

        last_month = datetime.now() - relativedelta(months=1)
        last_month_orders = Order.objects.filter(created_at__month=last_month.month)
        last_month_sales = last_month_orders.annotate(date=TruncDay('created_at')).values('date').annotate(total=Sum('paid_amount')).order_by('date')
        last_month_average = last_month_sales.aggregate(Avg('total'))['total__avg']

        max_sale = int(last_month_average) * 0.8
        # Преобразуем данные в формат, который требуется для SARIMAX
        sales = []
        for item in daily_sales:
            sale = item['total']
            # Ограничиваем значение продаж в диапазоне от 0 до avg_sales
            sale = np.clip(sale, 0, max_sale)
            sales.append(sale)

        # Создаем DataFrame и заполняем пропущенные значения средними значениями по столбцу
        df = pd.DataFrame({'sales': sales})
        df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
        df = df.fillna(df.mean())

        p = 1
        d = 1
        q = 1
        P = 1
        D = 1
        Q = 1

        # Создаем модель SARIMAX и обучаем ее на данных продаж
        model = SARIMAX(df, order=(p, d, q), seasonal_order=(P, D, Q, 12))
        model_fit = model.fit(disp=0)

        # Получаем прогноз на следующие 12 месяцев
        forecast = model_fit.forecast(steps=12)

        # Создаем список объектов прогнозов для каждого месяца
        forecast_data = []
        next_month = datetime.now().month + 1
        for i, value in enumerate(forecast.tolist()):
            year = datetime.now().year
            month = next_month + i
            if month > 12:
                year += 1
                month -= 12
            date = datetime(year, month, 1).strftime('%Y-%m')
            forecast_data.append({'date': date, 'value': value*30})

        # Возвращаем данные прогноза в формате JSON
        return JsonResponse(forecast_data, safe=False)






