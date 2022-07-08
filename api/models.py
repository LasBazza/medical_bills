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
    client_name = models.ForeignKey(
        Client,
        to_field='name',
        on_delete=models.CASCADE,
        verbose_name='Клиент',
        related_name='organizations'
    )
    address = models.CharField('Адрес', max_length=400)
    fraud_weight = models.IntegerField('Оценка мошенничества', default=0)

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
    client_name = models.ForeignKey(
        Client,
        to_field='name',
        on_delete=models.CASCADE,
        verbose_name='Клиент',
        related_name='bills'
    )
    organization = models.ForeignKey(
        Organization,
        to_field='name',
        on_delete=models.CASCADE,
        verbose_name='Организация'
    )
    fraud_score = models.FloatField('Оценка мошенничества')
    service_class = models.IntegerField('Номер класса услуги')
    service_name = models.CharField('Название класса услуги', max_length=200)

    class Meta:
        unique_together = ['number', 'organization']
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'

    def __str__(self):
        return f'{self.number} {self.organization.name}'


class ColumnNames(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    client_name_column = models.CharField('Название колонки клиента', max_length=200)
    organization_column = models.CharField('Название колонки организации', max_length=200)
    number_column = models.CharField('Название колонки номера счета', max_length=200)
    sum_column = models.CharField('Название колонки суммы', max_length=200)
    date_column = models.CharField('Название колонки даты', max_length=200)
    service_column = models.CharField('Название колонки услуги', max_length=200)

    class Meta:
        verbose_name = 'Название колонок'
        verbose_name_plural = 'Названия колонок'

    def __str__(self):
        return f'Колоноки клиента {self.client}'
