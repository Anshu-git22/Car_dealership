from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Car

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'user_type', 'password1', 'password2']
        
class CarForm(forms.ModelForm):

    class Meta:
        model = Car

        fields = [
            'brand',
            'model_name',
            'year',
            'fuel_type',
            'transmission',
            'engine',
            'price',
            'booking_amount',
            'kilometers_driven',
            'description',
            'image',
            'city',
        ]
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'phone',
            'user_type',
            'profile_image',
            'address',
        ]

        help_texts = {
            'username': '',
        }

        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl text-black'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-3 rounded-xl text-black'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl text-black'}),
            'user_type': forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-xl text-black'}),
            'profile_image': forms.FileInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-white text-black'}),
            'address': forms.Textarea(attrs={'class': 'w-full px-4 py-3 rounded-xl text-black', 'rows': 4}),
        }