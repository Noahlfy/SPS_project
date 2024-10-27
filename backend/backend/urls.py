from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from session.views import SessionViewSet
from chest.views import ChestViewSet
from head.views import HeadViewSet
from left_leg.views import LeftLegViewSet
from right_leg.views import RightLegViewSet
from temperature.views import TemperatureViewSet
from heart_rate.views import HeartRateViewSet

router = routers.DefaultRouter()
router.register("session", SessionViewSet)
router.register("chest", ChestViewSet)
router.register("head", HeadViewSet)
router.register("left-leg", LeftLegViewSet)
router.register("right-leg", RightLegViewSet)
router.register("temperature", TemperatureViewSet)
router.register("heart-rate", HeartRateViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
