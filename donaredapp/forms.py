from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Item, Zona, Categoria
import requests
from django.conf import settings

class UserRegistrationForm(UserCreationForm):
    """
    Form for user registration with additional fields
    """
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    movil = forms.CharField(max_length=15, required=False, help_text="Número de teléfono móvil (opcional)")
    validado = forms.BooleanField(
        required=False,
        label="Quiero ser validado para recibir donaciones",
        help_text="Marca esta casilla para habilitar recibir donaciones tras validación."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'movil', 'validado', 'first_name', 'last_name', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            # Save the mobile number to the user's profile
            user.profile.movil = self.cleaned_data['movil']
            #user.profile.validado = self.cleaned_data['validado']
            user.profile.save()
        return user
    
class PasswordRecoveryForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'id_email'})
    )

class ItemForm(forms.ModelForm):
    direccion = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la dirección completa',
            'id': 'direccion'
        })
    )

    class Meta:
        model = Item
        fields = ['nombre', 'descripcion', 'zona', 'categoria', 'imagen', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'zona': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion')
        if direccion:
            # Agregar "Buenos Aires, Argentina" para mejorar la precisión
            direccion_completa = f"{direccion}, Buenos Aires, Argentina"
            print(f"Intentando geocodificar: {direccion_completa}")
            
            # Usar Nominatim para geocodificación
            url = f"https://nominatim.openstreetmap.org/search"
            params = {
                'q': direccion_completa,
                'format': 'json',
                'limit': 1
            }
            headers = {
                'User-Agent': 'DonaRed/1.0'  # Identificador de la aplicación
            }
            
            try:
                response = requests.get(url, params=params, headers=headers)
                response.raise_for_status()
                data = response.json()
                print(f"Respuesta de geocodificación: {data}")
                
                if data:
                    # Guardar las coordenadas en el formulario para usarlas después
                    self.latitude = float(data[0]['lat'])
                    self.longitude = float(data[0]['lon'])
                    print(f"Coordenadas obtenidas: lat={self.latitude}, lon={self.longitude}")
                    return direccion
                else:
                    print("No se encontraron resultados de geocodificación")
                    raise forms.ValidationError("No se pudo encontrar la ubicación. Por favor, verifique la dirección.")
            except requests.RequestException as e:
                print(f"Error en la geocodificación: {str(e)}")
                raise forms.ValidationError("Error al validar la dirección. Por favor, intente nuevamente.")
        
        return direccion