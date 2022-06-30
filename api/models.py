from django.db import models


class Client(models.Model):
    name = models.CharField('Имя', max_length=150, unique=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField('Название', max_length=150, unique=True)
    client_name = models.ForeignKey(Client, to_field='name', on_delete=models.CASCADE, verbose_name='Клиент')
    address = models.CharField('Адрес', max_length=400)

    class Meta:
        unique_together = ['name', 'client_name']
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.name


class Bill(models.Model):
    number = models.IntegerField('Номер')
    sum = models.FloatField('Сумма')
    date = models.DateField('Дата')
    service = models.CharField('Услуга', max_length=400)
    client_name = models.ForeignKey(Client, to_field='name', on_delete=models.CASCADE, verbose_name='Клиент')
    client_org = models.ForeignKey(Organization, to_field='name', on_delete=models.CASCADE, verbose_name='Организация')

    class Meta:
        unique_together = ['number', 'client_org']
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'

    def __str__(self):
        return f'{self.number} {self.client_org.name}'
