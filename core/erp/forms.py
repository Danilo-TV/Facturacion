from django.forms import *

from core.erp.models import Category, Product


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

    # Elimina el método save() personalizado que retornaba un diccionario
