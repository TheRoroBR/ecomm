import re
from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(label='Nome de usuário')
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Senha',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repita a senha',
                                widget=forms.PasswordInput)
    
    # Profile fields
    cpf = forms.CharField(label='CPF', max_length=14, widget=forms.TextInput(attrs={'placeholder': '000.000.000-00'}))
    phone = forms.CharField(label='Telefone', max_length=15, widget=forms.TextInput(attrs={'placeholder': '(00) 00000-0000'}))
    postal_code = forms.CharField(label='CEP', max_length=9, widget=forms.TextInput(attrs={'placeholder': '00000-000'}))
    address = forms.CharField(label='Endereço', max_length=250)
    address_number = forms.CharField(label='Número', max_length=10)
    complement = forms.CharField(label='Complemento', max_length=100, required=False)
    city = forms.CharField(label='Cidade', max_length=100)
    state = forms.CharField(label='Estado', max_length=2)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Nome de usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('As senhas não coincidem.')
        return cd['password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('E-mail já está em uso.')
        return data

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        # Remove non-digits
        cpf = re.sub(r'\D', '', cpf)
        
        if len(cpf) != 11:
            raise forms.ValidationError('CPF deve conter 11 dígitos.')
        
        # Check if all digits are equal
        if len(set(cpf)) == 1:
            raise forms.ValidationError('CPF inválido.')

        # Validate digits
        for i in range(9, 11):
            value = sum((int(cpf[num]) * ((i + 1) - num) for num in range(0, i)))
            digit = ((value * 10) % 11) % 10
            if digit != int(cpf[i]):
                raise forms.ValidationError('CPF inválido.')
        return cpf

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        phone = re.sub(r'\D', '', phone)
        if len(phone) < 10 or len(phone) > 11:
            raise forms.ValidationError('Telefone inválido. Use o formato (DD) 99999-9999.')
        return phone

    def clean_postal_code(self):
        cep = self.cleaned_data['postal_code']
        cep = re.sub(r'\D', '', cep)
        if len(cep) != 8:
            raise forms.ValidationError('CEP inválido.')
        return cep


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Seu primeiro nome'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Seu sobrenome'}),
            'email': forms.EmailInput(attrs={'placeholder': 'seu@email.com'}),
        }

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id)\
                         .filter(email=data)
        if qs.exists():
            raise forms.ValidationError('E-mail já está em uso.')
        return data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo', 'cpf', 'phone', 'postal_code', 'address', 'address_number', 'complement', 'city', 'state']
        labels = {
            'date_of_birth': 'Data de nascimento',
            'photo': 'Foto',
            'cpf': 'CPF',
            'phone': 'Telefone',
            'postal_code': 'CEP',
            'address': 'Endereço',
            'address_number': 'Número',
            'complement': 'Complemento',
            'city': 'Cidade',
            'state': 'Estado',
        }
        widgets = {
            'photo': forms.FileInput(),
            'cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00'}),
            'phone': forms.TextInput(attrs={'placeholder': '(00) 00000-0000'}),
            'postal_code': forms.TextInput(attrs={'placeholder': '00000-000'}),
            'address': forms.TextInput(attrs={'placeholder': 'Rua, Avenida, etc.'}),
            'address_number': forms.TextInput(attrs={'placeholder': '123'}),
            'complement': forms.TextInput(attrs={'placeholder': 'Apto 101, Bloco B'}),
            'city': forms.TextInput(attrs={'placeholder': 'Sua cidade'}),
            'state': forms.TextInput(attrs={'placeholder': 'UF'}),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if not cpf: return cpf
        # Remove non-digits
        cpf = re.sub(r'\D', '', cpf)
        
        if len(cpf) != 11:
            raise forms.ValidationError('CPF deve conter 11 dígitos.')
        
        # Check if all digits are equal
        if len(set(cpf)) == 1:
            raise forms.ValidationError('CPF inválido.')

        # Validate digits
        for i in range(9, 11):
            value = sum((int(cpf[num]) * ((i + 1) - num) for num in range(0, i)))
            digit = ((value * 10) % 11) % 10
            if digit != int(cpf[i]):
                raise forms.ValidationError('CPF inválido.')
        return cpf

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone: return phone
        phone = re.sub(r'\D', '', phone)
        if len(phone) < 10 or len(phone) > 11:
            raise forms.ValidationError('Telefone inválido. Use o formato (DD) 99999-9999.')
        return phone

    def clean_postal_code(self):
        cep = self.cleaned_data['postal_code']
        if not cep: return cep
        cep = re.sub(r'\D', '', cep)
        if len(cep) != 8:
            raise forms.ValidationError('CEP inválido.')
        return cep
