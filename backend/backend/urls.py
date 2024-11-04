from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from session.views import SessionViewSet
from chest.views import ChestViewSet
from chest_transformed.views import ChestTransformedViewSet
from head.views import HeadViewSet
from head_transformed.views import HeadTransformedViewSet
from left_leg.views import LeftLegViewSet
from left_leg_transformed.views import LeftLegTransformedViewSet
from right_leg.views import RightLegViewSet
from right_leg_transformed.views import RightLegTransformedViewSet
from temperature.views import TemperatureViewSet
from heart_rate.views import HeartRateViewSet
from session_stats.views import SessionStatsViewSet
from concussion_stats.views import ConcussionStatsViewSet
from dashboard_stats.views import DashboardStatsViewSet
from chest_memory.views import ChestMemoryViewSet
from head_memory.views import HeadMemoryViewSet
from left_leg_memory.views import LeftLegMemoryViewSet
from right_leg_memory.views import RightLegMemoryViewSet

router = routers.DefaultRouter()
router.register("session", SessionViewSet)
router.register("chest", ChestViewSet)
router.register("chest-transformed", ChestTransformedViewSet)
router.register("head", HeadViewSet)
router.register("head-transformed", HeadTransformedViewSet)
router.register("left-leg", LeftLegViewSet)
router.register("left-leg-transformed", LeftLegTransformedViewSet)
router.register("right-leg", RightLegViewSet)
router.register("right-leg-transformed", RightLegTransformedViewSet)
router.register("temperature", TemperatureViewSet)
router.register("heart-rate", HeartRateViewSet)
router.register("session-stats", SessionStatsViewSet)
router.register("concussion-stats", ConcussionStatsViewSet)
router.register("dashboard-stats", DashboardStatsViewSet)
router.register("chest-memory", ChestMemoryViewSet)
router.register("head-memory", HeadMemoryViewSet)
router.register("right-leg-memory", RightLegMemoryViewSet)
router.register("left-leg-memory", LeftLegMemoryViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
