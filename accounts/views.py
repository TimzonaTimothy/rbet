from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate, login,logout
from main.views import *
from django.contrib.auth.decorators import login_required
from django.contrib import auth

def register(request):
    try:
        code = request.POST.get('ref_code')
        referred = Account.objects.get(code=code)
    except:
        pass
    if request.method == 'POST':
        
        form = RegistrationForm(request.POST)
        
        
        if form.is_valid():
            
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            
            
            if Account.objects.filter(email=email).exists():
                messages.warning(request, 'Email already exists')
                return redirect('/register')
            if Account.objects.filter(email=email, is_active=False).exists():
                messages.warning(request, 'Email already exists')
                return redirect('/register')
                
                
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username,password=password,)
            
            
            try:
                user.recommended_by = str(referred)

            except:
                pass
            user.save()
            
            
            
    
            
            #user_activation
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('main/account_verification_email.html', {
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Thank you for registrating with us. We have sent you a verification email to your email address. Please verify it.')
            return redirect('/register')

        else:
            messages.warning(request, 'Invalid Credentials')
    else:
        form =RegistrationForm()
        
        context= {
            'form':form,
        }
        return render(request, 'main/register.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('/home')
    
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']

            user = auth.authenticate(email=email, password=password)

            if user is not None:
                auth.login(request,user)
                messages.success(request, ', Welcome '+user.username)
                return HttpResponseRedirect('dashboard')
                 
            else:
                messages.error(request, 'Invalid credentials')
                return redirect('/login')
        else:
            return render(request, 'main/login.html', {})

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('/login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('/login')




def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required(login_url = 'home')
def dashboard(request):
    
    return render(request,'main/dashboard.html', {})