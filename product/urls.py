from product import views
from django.urls import path
from .views import is_admin


urlpatterns = [
    path('products/search/', views.search),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
    path('products/<slug:category_slug>/', views.CategoryDetail.as_view()),
    path('random-products/', views.RandomProducts.as_view()),
    path('products/', views.AllProductsList.as_view()),
    path('categories/', views.AllCategoriesList.as_view()),
    path('admin/products/', views.ProductListCreateView.as_view()),
    path('admin/products/<int:pk>/', views.ProductRetrieveUpdateDestroyView.as_view()),
    path('admin/products/<int:product_id>/sizes/<str:size_name>/', views.ProductSizeDeleteView.as_view()),
    path('admin/categories/', views.CategoryListCreateView.as_view()),
    path('admin/categories/<int:pk>/', views.CategoryRetrieveUpdateDestroyView.as_view()),
    path('is_admin/', is_admin),
    path('current_user/', views.CurrentUserView.as_view()),
    # path('forgot-password/', views.ForgotPasswordView.as_view()),




]
