from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
import requests
import re
import certifi
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup

from core.erp.forms import SaleForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from django.views.generic import CreateView

from core.erp.models import Sale, Product

def obtener_tasa_bcv():
    try:
        url = 'https://www.bcv.org.ve/'
        response = requests.get(url, timeout=5, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        dolar_div = soup.find('div', id='dolar')
        if dolar_div:
            centrado_div = dolar_div.find('div', class_='centrado')
            if centrado_div:
                strong = centrado_div.find('strong')
                if strong:
                    tasa_text = strong.text.strip()
                    tasa_text = re.sub(r'[^\d,\.]', '', tasa_text)
                    tasa_text = tasa_text.replace(',', '.')
                    tasa = float(tasa_text)
                    return tasa
    except Exception as e:
        print(f"Error al obtener la tasa: {e}")
    return None

class SaleCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('index')
    permission_required = 'erp.add_sale'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Product.objects.filter(name__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.name
                    data.append(item)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        tasa = obtener_tasa_bcv()
        context['tasa_bcv'] = tasa  # Valor completo, sin redondear
        context['tasa_bcv_display'] = round(tasa, 2) if tasa is not None else None  # Solo para mostrar
        return context