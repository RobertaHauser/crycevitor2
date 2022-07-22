from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading

from validate_email import validate_email
from django.urls import reverse
from .models import CustomUser

# Create your views here.
#@login_required
def home(request):
    return render(request,'index.html')


### EMAIL THREAD, tutorial Cryce - aula 28
class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


### SEND ACTIVATION EMAIL
def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Ative sua conta'
    email_body = render_to_string('authentication/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email]
                         )

    EmailThread(email).start()
"""
    if not settings.TESTING:
        EmailThread(email).start()
"""



### REGISTER
#@auth_user_should_not_access
def register(request):
    
    if request.method == "POST":
        context = {'has_error': False, 'data': request.POST}
        email = request.POST.get('email')
        #username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if len(password) < 6:
            messages.add_message(request, messages.ERROR,
                                 'A senha deve ter pelo menos 6 caracteres')
            context['has_error'] = True

        if password != password2:
            messages.add_message(request, messages.ERROR,
                                 'Senha incorreta')
            context['has_error'] = True

        if not validate_email(email):
            messages.add_message(request, messages.ERROR,
                                 'Digite um endereço de e-mail válido')
            context['has_error'] = True

        if CustomUser.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR,
                                 'E-mail já cadastado, escolha outro')
            context['has_error'] = True

        if not first_name:
            messages.add_message(request, messages.ERROR,
                                 'O campo nome é obrigatório')
            context['has_error'] = True

        if not last_name:
            messages.add_message(request, messages.ERROR,
                                 'O campo sobrenome é obrigatório')
            context['has_error'] = True


            #### TUTORIAL CRYCE TRULLY, AULA 29
            #return render(request, 'authentication/register.html', context, status=409)

        if context['has_error']:
            return render(request, 'authentication/register.html', context)

        #user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name)
        user = CustomUser.objects.create_user(email=email, first_name=first_name, last_name=last_name,password=password)
        user.set_password(password)
        user.save()

        send_activation_email(user, request)

        #messages.add_message(request, messages.SUCCESS,'Conta criada, você pode logar')
        messages.add_message(request, messages.SUCCESS,'Enviamos um e-mail para verificar sua conta')

        return redirect('login')
    
    return render(request, 'authentication/register.html')


def login_user(request):
    return render(request, 'authentication/login.html')


### LOGIN
#@auth_user_should_not_access
def login_user(request):

    if request.method == 'POST':
        context = {'data': request.POST}
        #username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        #user = authenticate(request, username=username, email=email, password=password)
        user = authenticate(request, email=email, password=password)
        
        
        if user and not user.is_email_verified:
            messages.add_message(request, messages.ERROR,
                                 'E-mail não confirmado, verifique sua caixa de e-mail (inclusive spam)')
            return render(request, 'authentication/login.html', context, status=401)
        

        if not user:
            messages.add_message(request, messages.ERROR,
                                 'Credenciais inválidas, tente novamente')
            return render(request, 'authentication/login.html', context, status=401)

        login(request, user)

        messages.add_message(request, messages.SUCCESS,
                             f'Bem-vindo {user.first_name}')

        return redirect(reverse('home'))

    return render(request, 'authentication/login.html')


### LOGOUT
def logout_user(request):

    logout(request)

    messages.add_message(request, messages.SUCCESS,
                         'Desconectado com sucesso')

    return redirect(reverse('login'))


### ACTIVATE USER
def activate_user(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))

        user = CustomUser.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'E-mail verificado, agora você pode fazer login')
        return redirect(reverse('login'))

    return render(request, 'authentication/activate-failed.html', {"user": user})


#@login_required
def password_change(request):
    return render(request,'authentication/password_change.html')