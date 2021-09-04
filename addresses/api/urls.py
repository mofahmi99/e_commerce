from rest_framework.routers import DefaultRouter
from addresses.api import views

router = DefaultRouter()
router.register('', views.AddressApi, basename='address')
urlpatterns = router.urls
