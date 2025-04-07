from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.forms.models import model_to_dict
from django.contrib.auth.mixins import LoginRequiredMixin  # Esto es lo correcto

from django.contrib import messages
from core.erp.forms import ClientForm
from core.erp.models import Client


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'client/list.html'
    form_class = ClientForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Clientes'
        context['entity'] = 'Clientes'
        context['form'] = ClientForm()  # Formulario para el modal
        context['create_url'] = reverse_lazy('erp:client_create')
        context['list_url'] = reverse_lazy('erp:client_list')
        return context


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = None  # Esto fuerza a que no use template

    def dispatch(self, request, *args, **kwargs):
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return HttpResponseBadRequest('Solo se permiten peticiones AJAX')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Devuelve error si se accede directamente por GET
        return HttpResponseNotAllowed(['POST'])

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({
            'success': True,
            'message': 'Cliente creado exitosamente!'
        })

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'errors': form.errors.get_json_data()
        }, status=400)


class ClientUpdateView(LoginRequiredMixin, UpdateView):  # Y aquí
    model = Client
    form_class = ClientForm
    template_name = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        client_data = {
            'id': self.object.id,
            'names': self.object.names,
            'surnames': self.object.surnames,
            'dni': self.object.dni,
            'date_birthday': self.object.date_birthday.strftime('%Y-%m-%d'),
            'gender': self.object.gender,
            'address': self.object.address,
            # Añade aquí todos los campos adicionales
        }
        return JsonResponse(client_data)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({
            'success': True,
            'message': 'Cliente actualizado exitosamente!',
            'redirect_url': str(reverse_lazy('erp:client_list'))
        })

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'errors': form.errors.get_json_data()
        }, status=400)

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'client/client_confirm_delete.html'
    success_url = reverse_lazy('erp:client_list')  # Asegúrate que 'erp:client_list' sea el nombre correcto

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Cliente eliminado exitosamente',
                'redirect_url': str(self.success_url)  # URL a la que redirigir
            })
        return super().post(request, *args, **kwargs)  # Para peticiones NO-AJAX (por si acaso)