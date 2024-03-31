from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

# path("menu-items", views.MenuItemsView.as_view()),
# path("menu-items/<int:pk>", views.SingleMenuItemView.as_view()),
urlpatterns = [
    #w3.filtering lab
    path('category', views.CategoriesView.as_view()),
    path('menu-items/', views.MenuItemsView.as_view()),

    # More on filtering and pagination.step2
    # path('menu-items',views.MenuItemsViewSet.as_view({'get':'list'})),
    path('menu-items/<int:pk>',views.MenuItemsViewSet.as_view({'get':'retrieve'})),

    # path("menu-items/", views.menu_items),
    # path("menu-items/<int:id>", views.single_item),
    
    path("category/<int:pk>", views.category_detail, name="category-detail"),
    path("menu", views.menu),
    path('welcome',views.welcome),
#Authentication
    path('secret/',views.secret,name='secret'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
