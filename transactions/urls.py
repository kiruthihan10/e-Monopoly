from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'transactions', views.TransactionViewSet)
router.register(r'games', views.GameViewSet)
router.register(r'players', views.PlayerViewSet)