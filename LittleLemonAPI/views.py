from rest_framework import generics
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework_csv.renderers import CSVRenderer
from rest_framework_yaml.renderers import YAMLRenderer

# Pagination
from django.core.paginator import Paginator, EmptyPage

# More on filtering and pagination.step1
from rest_framework.response import Response
from rest_framework import viewsets
from .models import MenuItem
from .serializers import MenuItemSerializer

# Authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

#Throttling
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import throttle_classes
from .throttles import TenCallsPerMinute

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ["price", "inventory"]
    filteset_fields = ["price", "inventory"]
    search_fields = ["title", "category__title"]
    # search_fields=['category']


class MenuItemsViewSet(viewsets.ModelViewSet):
  #  throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ["price", "inventory"]
    # search_fields=['title']
    search_fields = ["title", "category__title"]

    def get_throttles(self):
        if self.action == 'create':
            throttle_classes = [UserRateThrottle]
        else:
            throttle_classes = []
        return [throttle() for throttle in throttle_classes]

# Create your views here.
# class MenuItemsView(generics.ListCreateAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer


# class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer
#     # lookup_field = 'id'
from .models import Category
from .serializers import CategorySerializer


@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data)


@api_view(["GET", "POST"])
# @renderer_classes([CSVRenderer])
# @renderer_classes([YAMLRenderer])
def menu_items(request):
    if request.method == "GET":
        items = MenuItem.objects.select_related("category").all()
        category_name = request.query_params.get("category")
        to_price = request.query_params.get("to_price")
        search = request.query_params.get("search")
        ordering = request.query_params.get("ordering")

        # Pagination
        perpage = request.query_params.get("perpage", default=2)
        page = request.query_params.get("page", default=1)

        if search:
            items = items.filter(title__icontains=search)

        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price__lte=to_price)
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)

        # Pagination object inializing
        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []

        serialized_item = MenuItemSerializer(
            items,
            many=True,
            context={"request": request},
        )
        return Response(serialized_item.data)
    if request.method == "POST":
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)


# @api_view()
# def single_item(request, id):
#     item = MenuItem.objects.get(pk=id)
#     serialized_item = MenuItemSerializer(item)
#     return Response(serialized_item.data)


@api_view()
def single_item(request, id):
    item = get_object_or_404(MenuItem, pk=id)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data)


@api_view()
@renderer_classes([TemplateHTMLRenderer])
def menu(request):
    items = MenuItem.objects.select_related("category").all()
    serialized_item = MenuItemSerializer(items, many=True)
    return Response(
        {"data": serialized_item.data},
        template_name="menu_items.html",
    )


@api_view(["GET"])
@renderer_classes([StaticHTMLRenderer])
def welcome(request):
    data = "<html><body><h1>Welcome To Little Lemon API Project</h1></body></html>"
    return Response(data)


@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message": "Some secret message"})


@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name="Manager").exists():
        return Response({"message": "Only Manager should see this"})
    else:
        return Response({"message": "You are not a Manager"}, 403)

@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message": "successful"})


@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def throttle_check_auth(request):
    return Response({"message": "message for the logged in users only"})