from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('BookListDRF.urls')),
    # path('api/', include('LittleLemonAPI.urls')),
    # path('api/', include('BookListAPI.urls')),
    path('api/' ,include('LittleLemonDRF.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]
