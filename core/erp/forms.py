from datetime import datetime

from django.forms import *

from core.erp.models import Category, Product, Client


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'desc': Textarea(attrs={
                'placeholder': 'Ingrese una descripción',
                'rows': 3,
                'cols': 3
            }),
        }
        exclude = ['user_updated', 'user_creation']


class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese nombre del producto'}),
            'cate': Select(attrs={'class': 'form-control select2'}),
        }


class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Client
        fields = '__all__'
        wigets = {
            'names': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres'
                }
            ),
            'surnames': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'dni': TextInput(
                attrs={
                    'placeholder': 'Ingrese su DNI',
                }
            ),
            'date_birthday': DateInput(format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                }
            ),
            'address': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dirección',
                }
            ),
            'gender': Select()
        }
        exclude = ['user_updated', 'user_creation']