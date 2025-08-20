from rest_framework import serializers
from .models import Skill, Mission, Submission, UserSkill, CustomUser

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'description']

class MissionSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    skill_id = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), write_only=True, source='skill'
    )

    class Meta:
        model = Mission
        fields = [
            'id', 'skill', 'skill_id', 'title', 'description', 'xp_reward',
            'option_a', 'option_b', 'option_c', 'option_d', 'correct_option'
        ]
        read_only_fields = ['correct_option']  # не отдаём наружу изменение правильного ответа, если нужно — уберите

class UserSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    class Meta:
        model = UserSkill
        fields = ['id', 'skill', 'level', 'xp']

class SubmissionSerializer(serializers.ModelSerializer):
    mission = MissionSerializer(read_only=True)
    mission_id = serializers.PrimaryKeyRelatedField(
        queryset=Mission.objects.all(), write_only=True, source='mission'
    )

    class Meta:
        model = Submission
        fields = ['id', 'mission', 'mission_id', 'answer', 'is_correct', 'created_at']
        read_only_fields = ['is_correct', 'created_at']

class MeSerializer(serializers.ModelSerializer):
    user_skills = UserSkillSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'user_skills']
