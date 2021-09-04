from django.urls import path, include
from rest_framework.routers import DefaultRouter

from products.api import views
from products.api.views import CategoryViewSet

router = DefaultRouter()
router.register('product', views.ProductViewSet)
router.register('category', views.CategoryViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('list_by_category/', CategoryViewSet.as_view({'get': 'list_by_category'})),
    path('list_categories/', CategoryViewSet.as_view({'get': 'list_categories'}))

]
