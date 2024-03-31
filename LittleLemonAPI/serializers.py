from decimal import Decimal
from rest_framework import serializers
from .models import MenuItem
from .models import Category
from rest_framework.validators import UniqueValidator
from rest_framework.validators import UniqueTogetherValidator
import bleach

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
    # class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    stock = serializers.IntegerField(source="inventory")
    price_after_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    category = CategorySerializer(read_only=True)
    # category = serializers.HyperlinkedRelatedField(
    #     queryset=Category.objects.all(), view_name="category-detail"
    # )
    category_id = serializers.IntegerField(write_only=True)
    # Method 1: Conditions in the field
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=2)

    # Method:3 Using validate_field() method
    # def validate_price(self, value):
    #     if (value < 2):
    #         raise serializers.ValidationError('Price should not be less than 2.0')
    #     return value

    # def validate_stock(self, value):
    #     if (value < 0):
    #         raise serializers.ValidationError('Stock cannot be negative')
    #     return value

    # Method 4: Using the validate() method
    # def validate(self, attrs):
    #     if attrs["price"] < 2:
    #         raise serializers.ValidationError("Price should not be less than 2.0")
    #     if attrs["inventory"] < 0:
    #         raise serializers.ValidationError("Stock cannot be negative")
    #     return super().validate(attrs)

    # UniqueValidator v1
    # title = serializers.CharField(
    #     max_length=255, validators=[UniqueValidator(queryset=MenuItem.objects.all())]
    # )
    #To sanitize the title field v1
    # def validate_title(self, value):
    #     return bleach.clean(value)

    #To sanitize the title field v2
    def validate(self, attrs):
        attrs['title'] = bleach.clean(attrs['title'])
        if(attrs['price']<2):
            raise serializers.ValidationError('Price should not be less than 2.0')
        if(attrs['inventory']<0):
            raise serializers.ValidationError('Stock cannot be negative')
        return super().validate(attrs)
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
            "category_id",
        ]
        # Method 2: Using keyword arguments in the Meta class
        # extra_kwargs = {
        #     "price": {"min_value": 2},
        #     "inventory": {"min_value": 0},
        # }

        # UniqueValidator v2
        # extra_kwargs = {
        #     "title": {"validators": [UniqueValidator(queryset=MenuItem.objects.all())]}
        # }

        # UniqueTogetherValidator
        validators = [
            UniqueTogetherValidator(
                queryset=MenuItem.objects.all(), fields=["title", "category_id"]
            )
        ]

    def calculate_tax(self, product: MenuItem):
        return product.price * Decimal(1.1)


# to show all fields
# class MenuItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MenuItem
#         fields = ["id", "title", "price", "inventory"]
