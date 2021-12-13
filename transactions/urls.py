from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'money', views.TransactionViewSet,'Money')
router.register(r'games', views.GameViewSet,'Games')
router.register(r'players', views.PlayerViewSet,'Players')
router.register(r'history', views.TransactionHistoryViewSet,'History')