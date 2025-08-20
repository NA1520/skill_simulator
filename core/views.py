from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Skill, Mission, UserSkill, Submission
from .forms import CustomUserCreationForm

def get_theme(request):
    theme = request.GET.get('theme')
    if theme in ['dark', 'light']:
        return theme
    return 'light'

def home_view(request):
    skills = Skill.objects.all()[:6]

    # Форма регистрации для неавторизованного пользователя
    form = None
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('home')
        else:
            form = CustomUserCreationForm()

    theme = get_theme(request)
    return render(request, 'core/home.html', {
        'skills': skills,
        'theme': theme,
        'form': form
    })

@login_required
def skill_detail_view(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    user_skill, _ = UserSkill.objects.get_or_create(user=request.user, skill=skill)
    missions = skill.missions.all()
    theme = get_theme(request)
    return render(request, 'core/skill_detail.html', {
        'skill': skill,
        'user_skill': user_skill,
        'missions': missions,
        'theme': theme
    })

@login_required
def mission_view(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)
    theme = get_theme(request)

    # Следующая миссия по тому же навыку
    next_mission = Mission.objects.filter(skill=mission.skill, id__gt=mission.id).order_by('id').first()

    submission = Submission.objects.filter(user=request.user, mission=mission).order_by('-created_at').first()
    result = None

    if request.method == 'POST':
        answer = request.POST.get('option')
        is_correct = (answer == mission.correct_option)
        submission, _ = Submission.objects.get_or_create(user=request.user, mission=mission)
        submission.answer = answer
        submission.is_correct = is_correct
        submission.save()

        if is_correct:
            us, _ = UserSkill.objects.get_or_create(user=request.user, skill=mission.skill)
            us.add_xp(mission.xp_reward)
            result = f"Верно! +{mission.xp_reward} XP"
        else:
            result = "Неверный ответ."

    options = {
        'A': mission.option_a,
        'B': mission.option_b,
        'C': mission.option_c,
        'D': mission.option_d,
    }

    return render(request, 'core/mission_detail.html', {
        'mission': mission,
        'options': options,
        'submission': submission,
        'result': result,
        'theme': theme,
        'next_mission': next_mission
    })

@login_required
def profile_view(request):
    user_skills = UserSkill.objects.filter(user=request.user)
    return render(request, 'core/profile.html', {
        'user': request.user,
        'user_skills': user_skills
    })

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})