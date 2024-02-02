from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import viewsets
from products.models import Product, Review, Category, Feedback
from rest_framework.decorators import action
from rest_framework import status
from ..filters import ProductFilter
from rest_framework import viewsets, filters, status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from products.serializers import ProductSerializer, ReviewSerializer, CategorySerializer, FeedbackSerializer
from django_filters.rest_framework import DjangoFilterBackend


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request):
        page = request.query_params.get('page', 1)
        query = request.query_params.get('query', '')
        category_name = request.query_params.get('category', '')

        queryset = self.filter_queryset(self.get_queryset())

        if query and query != 'null':
            queryset = queryset.filter(name__icontains=query)
        if category_name and category_name != 'null':
            queryset = queryset.filter(category__name=category_name)

        paginator = Paginator(queryset, 30)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        serializer = self.get_serializer(products, many=True)
        return Response({'products': serializer.data, 'page': page, 'pages': paginator.num_pages})

    @action(
        detail=True, methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def create_review(self, request, pk=None):
        user = request.user
        product = get_object_or_404(Product, pk=pk)

        existing_review = Review.objects.filter(
            product=product, user=user).first()
        if existing_review:
            return Response({'detail': 'You have already reviewed this product'}, status=status.HTTP_400_BAD_REQUEST)

        data = {'product': product.id, 'user': user.id, **request.data}
        serializer = ReviewSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def recommended(self, request):
        recommended_products = Product.get_recommended_products()
        serializer = ProductSerializer(recommended_products, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == 'create_review':
            return [IsAuthenticated()]
        elif self.action == 'recommended':
            return [AllowAny()]
        return super().get_permissions()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsAdminOrReadOnly]


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    # permission_classes = [IsAdminOrReadOnly]
