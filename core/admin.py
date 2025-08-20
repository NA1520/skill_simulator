from django.contrib import admin
from .models import CustomUser, Skill, UserSkill, Mission, Submission

admin.site.register(CustomUser)
admin.site.register(Skill)
admin.site.register(UserSkill)
admin.site.register(Mission)
admin.site.register(Submission)
