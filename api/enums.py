import random

from django.db import models


class ServiceClass(models.IntegerChoices):

    CONSULTATION = 1, 'консультация'
    TREATMENT = 2, 'лечение'
    HOSPITAL = 3, 'стационар'
    DIAGNOSING = 4, 'диагностика'
    LABORATORY = 5, 'лаборатория'

    @classmethod
    def get_random(cls):
        return random.choice(list(ServiceClass))
