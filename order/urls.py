from django.urls import path
from order import views

urlpatterns = [
    path('checkout/', views.checkout),
    path('my-orders/', views.MyOrdersList.as_view()), 
    path('admin/orders/', views.AdminOrderList.as_view()), 
    path('admin/orders/<int:pk>/', views.AdminOrderListDelete.as_view()), 
    path('admin/orders/chart/', views.OrderChartView.as_view()),
    path('admin/orders/month-forecast/', views.MonthSalesForecastView.as_view()),
    path('admin/orders/year-forecast/', views.YearSalesForecastView.as_view()),

]