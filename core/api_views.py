from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F
from .models import Skill, Mission, Submission, UserSkill
from .serializers import (
    SkillSerializer, MissionSerializer, SubmissionSerializer,
    UserSkillSerializer, MeSerializer
)

class IsTeacherOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and getattr(request.user, 'role', '') == 'teacher'

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all().order_by('id')
    serializer_class = SkillSerializer
    permission_classes = [IsTeacherOrReadOnly]

class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.select_related('skill').all().order_by('id')
    serializer_class = MissionSerializer
    permission_classes = [IsTeacherOrReadOnly]

class UserSkillViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSkillSerializer
    def get_queryset(self):
        return UserSkill.objects.filter(user=self.request.user).select_related('skill').order_by('skill__name')

class SubmissionViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user).select_related('mission', 'mission__skill').order_by('-created_at')

    def perform_create(self, serializer):
        sub = serializer.save(user=self.request.user)
        # Проверяем ответ
        is_correct = (sub.answer == getattr(sub.mission, 'correct_option'))
        sub.is_correct = is_correct
        sub.save()
        if is_correct:
            us, _ = UserSkill.objects.get_or_create(user=self.request.user, skill=sub.mission.skill)
            us.add_xp(sub.mission.xp_reward)

class MeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def profile(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data)
