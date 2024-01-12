from django.contrib.auth.views import LoginView, LogoutView

from django.conf import settings


# Superuser account
# username: rifki.gusti
# password: hbz934115

class LoginView(LoginView):
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True
    extra_context = {
        'title' : 'Login Page'
    }

class LogoutView(LogoutView):
    print('Hello world')
    next_page = settings.LOGIN_URL
    extra_context = {
        'page_header' : 'Halaman Login'
    }