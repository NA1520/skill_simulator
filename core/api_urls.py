from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import SkillViewSet, MissionViewSet, SubmissionViewSet, UserSkillViewSet, MeViewSet

router = DefaultRouter()
router.register(r'skills', SkillViewSet, basename='skills')
router.register(r'missions', MissionViewSet, basename='missions')
router.register(r'submissions', SubmissionViewSet, basename='submissions')
router.register(r'user-skills', UserSkillViewSet, basename='user-skills')

# отдельный маршрут на профиль
me_profile = MeViewSet.as_view({'get': 'profile'})

urlpatterns = [
    path('', include(router.urls)),
    path('me/', me_profile, name='me-profile'),
]
