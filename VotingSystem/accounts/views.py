from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .forms import UserRegistrationForm, LoginForm, VerificationCodeForm
from .models import User, VerificationCode
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.is_verified = False  # Require verification
            user.save()
            
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            registration_number = form.cleaned_data.get('registration_number')
            
            user = User.objects.filter(email=email, registration_number=registration_number).first()
            
            if user:
                # Remove any previous unused verification codes
                VerificationCode.objects.filter(user=user, is_used=False).delete()
                
                # Create new verification code
                verification_code = VerificationCode.objects.create(user=user)
                
                # Send verification email
                try:
                    send_mail(
                        'Verification Code for Online Voting System',
                        f'Your verification code is: {verification_code.code}\n\n'
                        'This code will expire in 30 minutes.',
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
                except Exception as e:
                    messages.error(request, 'Failed to send verification code. Please try again.')
                    return redirect('login')
                
                # Store verification information in session
                request.session['verification_data'] = {
                    'user_id': user.id,
                    'email': user.email
                }
                
                return redirect('verify_code')
            
            messages.error(request, 'Invalid email or registration number.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def verify_code(request):
    # Retrieve verification data from session
    verification_data = request.session.get('verification_data')

    # If no verification data, redirect to login
    if not verification_data:
        messages.error(request, 'Please initiate the login process again.')
        return redirect('login')

    try:
        # Retrieve user based on stored ID
        user_id = verification_data.get('user_id')
        email = verification_data.get('email')

        if not user_id or not email:
            messages.error(request, 'Invalid verification attempt.')
            return redirect('login')

        user = User.objects.get(id=user_id, email=email)
    except User.DoesNotExist:
        messages.error(request, 'User not found. Please log in again.')
        return redirect('login')

    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')

            # Find a valid verification code
            verification_code = VerificationCode.objects.filter(
                user=user,
                code=code,
                is_used=False,
                expires_at__gt=timezone.now()
            ).first()

            if verification_code:
                # Mark code as used
                verification_code.is_used = True
                verification_code.save()

                # Log in the user
                login(request, user)

                # Check if user is authenticated
                print(f"User authenticated: {request.user.is_authenticated}")  # Debugging line

                # Safely delete the session key
                if 'verification_data' in request.session:
                    del request.session['verification_data']

                messages.success(request, 'Verification successful!')
                return redirect('dashboard')  # Redirect to the dashboard

            messages.error(request, 'Invalid or expired verification code.')
    else:
        form = VerificationCodeForm()

    return render(request, 'registration/verify_code.html', {'form': form})
@login_required
def dashboard(request):
    return render(request, 'registration/dashboard.html', {'user': request.user})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

