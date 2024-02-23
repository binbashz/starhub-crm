from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import SignupForm
from .models import Userprofile
from team.models import Team, Plan 
from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                messages.error(request, 'The user with this username or email already exists.')
                return redirect('signup')

            user = form.save()
            plan_id = form.cleaned_data['plan']
            plan = Plan.objects.get(id=plan_id)
            team = Team.objects.create(name='The team name', created_by=user, plan=plan)
            team.members.add(user)
            team.save()
            Userprofile.objects.create(user=user, active_team=team)
            login(request, user)
            return redirect('/log-in/')
    else:
        form = SignupForm()
    return render(request, 'userprofile/signup.html', {'form': form})

@login_required
def myaccount(request):
    return render(request, 'userprofile/myaccount.html')

