from django.urls import path , include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

from .views import (
    VenueView , EventView
)

router.register(r'veune', VenueView, basename='user')
router.register(r'event', EventView, basename='user')



urlpatterns = router.urls

urlpatterns = [
    path('' , include(router.urls) ),
]
