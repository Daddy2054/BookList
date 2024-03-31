from django.urls import path
from . import views

# path("menu-items", views.MenuItemsView.as_view()),
# path("menu-items/<int:pk>", views.SingleMenuItemView.as_view()),
urlpatterns = [
    path("menu-items/", views.menu_items),
    path("menu-items/<int:id>", views.single_item),
    path("category/<int:pk>", views.category_detail, name="category-detail"),
    path("menu", views.menu),
    path('welcome',views.welcome)
]