from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import ProductForm
from core.erp.models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'product/list.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Productos'
        context['create_url'] = reverse_lazy('erp:product_create')
        context['list_url'] = reverse_lazy('erp:product_list')
        context['entity'] = 'Productos'
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('erp:product_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Maneja un formulario válido"""
        response = super().form_valid(form)
        messages.success(self.request, '¡Producto creado exitosamente!')
        return response

    def form_invalid(self, form):
        """Maneja un formulario inválido"""
        messages.error(self.request, 'Por favor corrija los errores a continuación')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de Producto'
        context['entity'] = 'Productos'
        context['list_url'] = self.success_url
        return context



class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('erp:product_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Maneja formulario válido con más detalles"""
        product_name = form.cleaned_data.get('name', 'el producto')
        messages.success(
            self.request,
            f'¡Producto "{product_name}" actualizado correctamente!'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        """Proporciona feedback más detallado"""
        error_count = len(form.errors)
        messages.error(
            self.request,
            f'Error: {error_count} campo(s) con errores. Por favor revise los datos.'
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': f'Edición de {self.object.name}',
            'entity': 'Productos',
            'list_url': self.success_url,
            'action': 'edit'  # Útil para el template
        })
        return context


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product/delete.html'
    success_url = reverse_lazy('erp:product_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        product_name = self.object.name
        try:
            self.object.delete()
            messages.success(
                request,
                f'¡Producto "{product_name}" fue eliminado permanentemente!'
            )
        except ProtectedError as e:
            messages.error(
                request,
                f'No se puede eliminar "{product_name}" porque tiene registros asociados'
            )
        except Exception as e:
            messages.error(
                request,
                f'Error inesperado al eliminar: {str(e)}'
            )
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': f'Eliminar {self.object.name}',
            'entity': 'Productos',
            'list_url': self.success_url,
            'confirmation_message': (
                f'¿Está seguro de eliminar permanentemente '
                f'"{self.object.name}" (ID: {self.object.id})? '
                '¡Esta acción no se puede deshacer!'
            )
        })
        return context