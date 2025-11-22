from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Data de Nascimento')
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True, verbose_name='Foto')
    
    # New fields
    cpf = models.CharField(max_length=14, blank=True, null=True, verbose_name='CPF')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Telefone')
    postal_code = models.CharField(max_length=9, blank=True, null=True, verbose_name='CEP')
    address = models.CharField(max_length=250, blank=True, null=True, verbose_name='Endereço')
    address_number = models.CharField(max_length=10, blank=True, null=True, verbose_name='Número')
    complement = models.CharField(max_length=100, blank=True, null=True, verbose_name='Complemento')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Cidade')
    state = models.CharField(max_length=2, blank=True, null=True, verbose_name='Estado')

    def __str__(self):
        return f'Profile of {self.user.username}'