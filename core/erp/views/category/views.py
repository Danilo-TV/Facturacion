from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from core.erp.forms import CategoryForm
from core.erp.mixins import IsSuperuserMixin
from core.erp.models import Category


class CategoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'erp.view_category'
    model = Category
    template_name = 'category/list.html'

    @method_decorator(csrf_exempt)
    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Category.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Categorías'
        context['create_url'] = reverse_lazy('erp:category_create')
        context['list_url'] = reverse_lazy('erp:category_list')
        context['entity'] = 'Categorias'
        return context


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/create.html'
    success_url = reverse_lazy('erp:category_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Maneja un formulario válido"""
        try:
            # Esto ahora guardará correctamente y retornará la instancia
            self.object = form.save()
            messages.success(self.request, '¡Categoría creada exitosamente!')
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Error al crear: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        error_messages = []
        for field, errors in form.errors.items():
            error_messages.append(f"{form.fields[field].label}: {', '.join(errors)}")

        messages.error(self.request, " | ".join(error_messages))
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación una Categoria'
        context['entity'] = 'Categorias'
        context['list_url'] = reverse_lazy('erp:category_list')
        return context


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/create.html'
    success_url = reverse_lazy('erp:category_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Maneja un formulario válido"""
        messages.success(self.request, '¡Categoría actualizada correctamente!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Maneja un formulario inválido"""
        messages.error(self.request, 'Por favor corrija los errores en el formulario')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición una Categoria'
        context['entity'] = 'Categorias'
        context['list_url'] = reverse_lazy('erp:category_list')
        return context


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category/delete.html'
    success_url = reverse_lazy('erp:category_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            self.object.delete()
            messages.success(request, '¡Registro eliminado correctamente!')
            return redirect(self.success_url)
        except Exception as e:
            messages.error(request, f'Error al eliminar: {str(e)}')
            return redirect(self.success_url)  # O puedes renderizar el template nuevamente

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Categoria'
        context['entity'] = 'Categorias'
        context['list_url'] = reverse_lazy('erp:category_list')
        return context


# class CategoryFormView(FormView):
#     form_class = CategoryForm
#     template_name = 'category/create.html'
#     success_url = reverse_lazy('erp:category_list')
#
#     def form_valid(self, form):
#         print(form.is_valid())
#         print(form)
#         return super().form_valid(form)
#
#     def form_invalid(self, form):
#         print(form.is_valid())
#         print(form.errors)
#         return super().form_invalid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Form | Categoria'
#         context['entity'] = 'Categorias'
#         context['list_url'] = reverse_lazy('erp:category_list')
#         context['action'] = 'add'
#         return context