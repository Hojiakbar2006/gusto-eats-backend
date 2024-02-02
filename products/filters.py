from django_filters import rest_framework as filters
from .models import Product, Category


class ProductFilter(filters.FilterSet):
    category = filters.ModelChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        to_field_name='name',
    )

    class Meta:
        model = Product
        fields = ['category']
