from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from .forms import RegisterForm


class RegisterView(SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('accounts:login')
    success_message = 'Cuenta creada exitosamente. Ya puedes iniciar sesión.'
