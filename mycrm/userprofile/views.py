from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, ProfileForm
from .models import Userprofile
from team.models import Team, Plan 
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy

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
    user_profile = request.user.userprofile
    return render(request, 'userprofile/myaccount.html', {'user_profile': user_profile})

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Userprofile
    form_class = ProfileForm
    template_name = 'userprofile/myaccount.html'
    success_url = reverse_lazy('myaccount')

    def get_object(self):
        return self.request.user.userprofile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()  # Pasa el formulario al contexto
        return context
