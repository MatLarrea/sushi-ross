from rest_framework import routers
from pedidos.api import ProjectDefaultView

router = routers.DefaultRouter()
router.register('SushiRoss', ProjectDefaultView, 'sushiross')
urlpatterns = router.urls