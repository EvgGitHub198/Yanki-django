from django.urls import path
from order import views

urlpatterns = [
    path('checkout/', views.checkout),
    path('my-orders/', views.MyOrdersList.as_view()), 
    path('admin/orders/', views.AdminOrderList.as_view()), 
    path('admin/orders/<int:pk>/', views.AdminOrderListDelete.as_view()), 
]