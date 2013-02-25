from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

from accounts.forms import UserForm, NewUserForm


def register(request):
    if request.user.is_authenticated():
        return redirect('accounts.views.profile')
        
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
    pwd_form = PasswordChangeForm(request.user)
    
    associations = {'twitter': False, 'google_oauth2': False, 'github': False}
    for association in request.user.social_auth.all():
        associations[association.provider.replace('-', '_')] = True
    
    if request.method == 'POST':
        if request.POST.get('do_password'):
            pwd_form = PasswordChangeForm(request.user, request.POST)

            if pwd_form.is_valid():
                pwd_form.save()
                messages.success(request, "Password successfully changed.")
            else:
                messages.error(request, "Could not update password. See errors below.")
        elif request.POST.get('do_profile'):
            form = UserForm(request.POST, instance=request.user)
        
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile successfully updated.')
            else:
                messages.error(request, 'You have an error in your profile. See below errors.')
        else:
            messages.error(request, "Er, something weird happened. Contact the site admin.")
        
    
    return render(request, 'accounts/profile.html', locals())

@login_required
def delete(request):
    request.user.delete()
    return redirect('/')

