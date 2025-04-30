from django.urls import path
from .views import SignUpView, LoginView, logout_view, get_csrf_token_view, HomeView,  UserProfileView, PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('csrf/', get_csrf_token_view, name='get_csrf_token'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]