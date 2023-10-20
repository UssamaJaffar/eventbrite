from django.urls import path , include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

from .views import (
    RegisterUserview , UserLoginView ,UserlogoutView ,
)

router.register(r'registeruser', RegisterUserview, basename='user')
router.register(r'login', UserLoginView, basename='user')
router.register(r'logout', UserlogoutView, basename='user')


urlpatterns = router.urls

urlpatterns = [
    path('' , include(router.urls) ),
]
