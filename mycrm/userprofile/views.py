from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import SignupForm
from .models import Userprofile

from team.models import Team, Plan # Importar el modelo de plan

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()

            plan_id = form.cleaned_data['plan'] # Obtener el valor del plan
            plan = Plan.objects.get(id=plan_id) # Buscar el objeto plan
            team = Team.objects.create(name='The team name', created_by=user, plan=plan) # Asignar el plan al equipo
            team.members.add(user)
            team.save()
            
            Userprofile.objects.create(user=user, active_team=team)

            return redirect('/log-in/')
    else:
        form = SignupForm()

    return render(request, 'userprofile/signup.html', {
        'form': form
    })

@login_required
def myaccount(request):
    return render(request, 'userprofile/myaccount.html')
