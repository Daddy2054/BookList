from decimal import Decimal
from rest_framework import serializers
from .models import MenuItem
from .models import Category


# # to hide some fields from json
# class MenuItemSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(max_digits=6, decimal_places=2)
#     inventory = serializers.IntegerField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "slug",
            "title",
        ]


class MenuItemSerializer(serializers.ModelSerializer):
#class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    stock = serializers.IntegerField(source="inventory")
    price_after_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    category = CategorySerializer(read_only=True)
    # category = serializers.HyperlinkedRelatedField(
    #     queryset=Category.objects.all(), view_name="category-detail"
    # )
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = MenuItem
        depth = 1
        fields = [
            "id",
            "title",
            "price",
            "stock",
            "price_after_tax",
            "category",
            'category_id',
        ]

    def calculate_tax(self, product: MenuItem):
        return product.price * Decimal(1.1)


# to show all fields
# class MenuItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MenuItem
#         fields = ["id", "title", "price", "inventory"]