import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import SignUpForm, LoginForm
from django.http import JsonResponse  # Import JsonResponse
from django.middleware.csrf import get_token
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from rest_framework.authtoken.models import Token
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail

class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'accounts/signup.html', {'form': form})

    def post(self, request):
        try:
            data = json.loads(request.body)  # Load JSON data from request.body
            form = SignUpForm(data)
            if form.is_valid():
                user = form.save()
                login(request, user)
                #  return redirect('home')  #  Change to JsonResponse
                return JsonResponse({'success': True, 'redirect': '/accounts/home/'}) # Return JSON for AJAX
            else:
                # return render(request, 'accounts/signup.html', {'form': form}) # Change to JsonResponse
                return JsonResponse({'errors': form.errors}, status=400) # Return JSON for AJAX
        except json.JSONDecodeError:
            # return render(request, 'accounts/signup.html', {'form': form})
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

class LoginView(View):
    def get(self, request):
        #form = LoginForm()
        #return render(request, 'accounts/login.html', {'form': form})
        try:
            template = get_template('accounts/login.html')  # This will raise an error if the template is not found
            print(f"Template found: {template.origin}")  # Print the template path if found
        except Exception as e:
            print(f"Template error: {e}")  # Print the error if the template is not found
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})
    def post(self, request):
        try:
            data = json.loads(request.body)
            form = LoginForm(data)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    # Generate or retrieve token
                    token, _ = Token.objects.get_or_create(user=user)
                    return JsonResponse({'success': True, 'token': token.key, 'redirect': '/accounts/home/'})
                else:
                    return JsonResponse({'error': 'Invalid credentials'}, status=401)
            else:
                return JsonResponse({'errors': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
    def get(self, request):
        user = request.user
        return JsonResponse({
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })
    
def logout_view(request):
    logout(request)
    return redirect('home')  #  Keep as a redirect,  or change to JsonResponse if needed by your frontend

@login_required
def home_view(request):
    return render(request, 'accounts/home.html') # A simple protected page

def get_csrf_token_view(request):
    """Returns the CSRF token as a JSON response."""
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

class PasswordResetRequestView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            form = PasswordResetForm({'email': email})
            if form.is_valid():
                form.save(
                    request=request,
                    use_https=True,
                    email_template_name='accounts/password_reset_email.html',
                )
                return JsonResponse({'success': True, 'message': 'Password reset email sent.'})
            else:
                return JsonResponse({'errors': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

class PasswordResetConfirmView(View):
    def post(self, request, uidb64, token):
        try:
            data = json.loads(request.body)
            new_password = data.get('new_password')
            user = User.objects.get(pk=uidb64)
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return JsonResponse({'success': True, 'message': 'Password has been reset.'})
            else:
                return JsonResponse({'error': 'Invalid token or user ID.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)