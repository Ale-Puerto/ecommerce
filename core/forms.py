from django import forms
from .models import Direccion

from django_countries.fields  import CountryField
from phone_field.forms import *
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from django_countries.widgets import CountrySelectWidget


class DireccionForm(forms.Form):
    nombre_referencia = forms.CharField(max_length=100, required=False,
                                        widget=forms.TextInput(attrs={
                                            "class" : "form-control",
                                            'placeholder' : 'Example Pedro Pedrito Pedrote'
                                        })
                                        )
    telefono =PhoneNumberField(required=False, widget=PhoneNumberInternationalFallbackWidget(attrs={
                                    'class' : 'form-control '
                                }))
    direccion_especifica = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={
                                            'class' : 'form-control',
                                            'placeholder' : 'NY, street 4th',


                                            }))
    apartamento = forms.CharField(max_length=50, required=False)
    pais = CountryField(blank_label='(Select country)').formfield(required=False, 
                                                                 widget=CountrySelectWidget(attrs={
                                                                     'class':'custom-select d-block w-100'
                                                                 }))
    provincia = forms.CharField(required=False, widget=forms.TextInput(attrs={
                                    'class':'form-control '
                                }))
    ciudad = forms.CharField(required=False, widget=forms.TextInput(attrs={
                                'class':'form-control'
                            }))
    codigo_postal = forms.CharField(required=False, widget=forms.TextInput(attrs={
                                            'class':'form-control '
                                        }))

    default = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
                                    
                                }))
    guardar = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
                                }))


class CuponForm(forms.Form):
    codigo = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={
                                'class':'form-control',
                                'placeholder' : 'Codigo de cupon'
                            }))

class PagoForm(forms.Form):
    """PagoForm definition."""
    stripeToken = forms.CharField()
    save = forms.BooleanField()
    use_default = forms.BooleanField()
    


