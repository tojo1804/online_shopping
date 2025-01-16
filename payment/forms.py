from django import forms
from .models import ShippingAdress

class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'custom-input','placeholder':'Full name'}),required=True,error_messages={'required': 'Veuillez remplir ce champ.'})
    shipping_email = forms.EmailField(label="",widget=forms.TextInput(attrs={'class': 'custom-input','placeholder': 'Email'}),required=False)
    shipping_addresse = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'custom-input','placeholder': 'Address'}),required=True,error_messages={'required': 'Veuillez remplir ce champ.'})
    shipping_city = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'custom-input','placeholder': 'City'}),required=True,error_messages={'required': 'Veuillez remplir ce champ.'})
    shipping_zipcode = forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'custom-input','placeholder': 'Zipcode'}),required=False)
    shipping_numberphone =forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'custom-input','type': 'tel','placeholder': 'Numero de telephone'}),required=True,error_messages={'required': 'Veuillez remplir ce champ.'})
    class Meta:
        model = ShippingAdress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_addresse', 'shipping_city', 'shipping_zipcode','shipping_numberphone']
        exclude=["user"] 



class PaymentForm(forms.Form):
    card_name=forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'custom-input','placeholder': 'Nom de carte'}),required=True)
    card_number=forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'custom-input','placeholder': 'Numero de carte'}),required=True)
    card_exp_date=forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'custom-input','placeholder': 'Date dexpiration '}),required=True)
    card_cvv=forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'custom-input','placeholder': 'carte cvv'}),required=True)
    card_adress=forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'custom-input','placeholder': 'Address carte'}),required=True)
    number_phone=forms.CharField(label="",widget=forms.TextInput(attrs={'class': 'custom-input','placeholder': 'Numero telephone'}),required=True)