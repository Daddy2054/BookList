from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('api/', include('BookListDRF.urls')),
    path("api/", include("LittleLemonAPI.urls")),
    # path('api/', include('BookListAPI.urls')),
    # path('api/' ,include('LittleLemonDRF.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
    # Djoser
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    # JWT
    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "api/token/blacklist/",
        TokenBlacklistView.as_view(),
        name="token_blacklist",
    ),
]
