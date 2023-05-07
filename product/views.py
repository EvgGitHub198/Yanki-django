import random
from rest_framework import generics, status
from django.http import Http404
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Category, ProductSize, Size
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.decorators import api_view, permission_classes
from django.core.cache import cache



class AllProductsList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class AllCategoriesList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer    

class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404
        
    def get(self, request, category_slug, format=None):
        category= self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({'products': []})
    

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser,)
    parser_classes = [MultiPartParser, JSONParser, FormParser]




class ProductSizeDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAdminUser,)
    queryset = ProductSize.objects.all()

    def delete(self, request, *args, **kwargs):
        product_id = kwargs['product_id']
        size_name = kwargs['size_name']

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            size = Size.objects.get(name=size_name)
        except Size.DoesNotExist:
            return Response({"error": "Size not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            product_size = ProductSize.objects.get(product=product, size=size)
            # Check if there are other sizes available for this product
            other_sizes = ProductSize.objects.filter(product=product).exclude(id=product_size.id)
            if other_sizes.exists():
                product_size.delete()
            else:
                product.delete()
        except ProductSize.DoesNotExist:
            return Response({"error": "Product size not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"success": "Product size deleted"})



class GetProductById(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer




class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)



class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser,)

    def put(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            if 'category_image' not in request.data:
                serializer.validated_data.pop('category_image', None)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class RandomProducts(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        random_products = random.sample(list(products), 4)
        serializer = ProductSerializer(random_products, many=True)
        return Response(serializer.data)


class CheckProductsAPIView(APIView):
    def post(self, request):
        product_ids = request.data.get('products_id', [])  # Получение списка идентификаторов продуктов из запроса

        # Проверка наличия продуктов в базе данных
        existing_products = Product.objects.filter(id__in=product_ids).values_list('id', flat=True)

        # Сравнение переданных идентификаторов с найденными в базе данных
        missing_products = list(set(product_ids) - set(existing_products))

        if missing_products:
            # Если есть отсутствующие продукты, возвращаем ошибку
            return Response({'error': f'Товары с идентификаторами {missing_products} не найдены в базе данных.'}, status=400)
        else:
            # Если все продукты найдены, возвращаем успешный результат
            return Response({'message': 'Все продукты найдены в базе данных.'}, status=200)
        

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response({'user_id': request.user.id})
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_admin(request):
    is_admin = IsAdminUser().has_permission(request, None)
    cache_key = f'is_admin:{request.user.pk}'
    cache.set(cache_key, is_admin, timeout=60 * 5) # кэш на 5 минут
    return Response({'is_admin': is_admin})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    cache_key = f'is_admin:{request.user.pk}'
    cache.delete(cache_key)
    return Response({'success': True})


