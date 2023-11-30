from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import CreateUserView
# from quickstart import views

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
urlpatterns = router.urls
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns += [
    path("admin/", admin.site.urls),
    # path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('imdb/', include('imdb.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', CreateUserView.as_view(), name='create_user'),
]

