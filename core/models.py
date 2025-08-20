from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Пользователь с ролью
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    role = models.CharField(max_length=7, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return self.username

# Навык
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name

# Навык пользователя с уровнем и XP
class UserSkill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='user_skills')
    level = models.PositiveIntegerField(default=1)
    xp = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'skill')

    def __str__(self):
        return f"{self.user} / {self.skill} — lvl {self.level} ({self.xp} XP)"

    # Метод добавления опыта и повышения уровня
    def add_xp(self, amount: int):
        self.xp += amount
        while self.xp >= self.level * 100:
            self.xp -= self.level * 100
            self.level += 1
        self.save()

# Миссия
class Mission(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='missions')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    xp_reward = models.PositiveIntegerField(default=10)
    option_a = models.CharField(max_length=200, blank=True, default='')
    option_b = models.CharField(max_length=200, blank=True, default='')
    option_c = models.CharField(max_length=200, blank=True, default='')
    option_d = models.CharField(max_length=200, blank=True, default='')
    correct_option = models.CharField(max_length=1, blank=True, default='A')  # хранит букву A/B/C/D

    def __str__(self):
        return f"{self.skill.name} — {self.title}"

# Отправка ответа пользователя на миссию
class Submission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='submissions')
    answer = models.CharField(max_length=255, blank=True, default='')
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'mission')

    def __str__(self):
        return f"{self.user} -> {self.mission} ({'✓' if self.is_correct else '✗'})"
