from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from accounts.forms import UserForm, NewUserForm


def register(request):
    form = NewUserForm()
    if request.POST:
        form = NewUserForm(request.POST)
        
        if form.is_valid():
            new_user = form.save()
            messages.success(request, "Account created! Now log in.")
            return redirect('django.contrib.auth.views.login')
        else:
            messages.error(request, "Your form had errors. See below.")
    
    return render(request, 'accounts/signup.html', locals())

@login_required
def profile(request):
    form = UserForm(instance=request.user)
    
    associations = {'twitter': False, 'google_oauth2': False, 'github': False}
    for association in request.user.social_auth.all():
        associations[association.provider.replace('-', '_')] = True
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        
        if 'delete_user' in request.POST.keys():
            request.user.delete()
            return redirect('/')
        
        if form.is_valid():
            form.save()
            messages.success(request, 'User successfully updated.')
        else:
            messages.error(request, 'You have an error in your profile. See below errors.')
        
    
    return render(request, 'accounts/profile.html', locals())

