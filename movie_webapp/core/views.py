from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html',{
        'form':form 
    })

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')