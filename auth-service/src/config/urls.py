from django.contrib import admin
from django.urls import include, path
from users.urls import router as user_router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(user_router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
