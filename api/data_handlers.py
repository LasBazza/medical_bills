import random

from api.enums import ServiceClass

from .models import Bill, Organization


def fraud_check(value: str) -> float:
    return random.uniform(0, 1)


def service_classifier(value: str) -> dict:
    result = ServiceClass.get_random()
    return {result.value: result.label}


def bills_annotate(bills: list[dict]) -> None:
    for bill in bills:
        bill['fraud_score'] = fraud_check(bill['service'])
        service_class_dict = service_classifier(bill['service'])
        bill['service_class'],  bill['service_name'] = list(service_class_dict.items())[0]


def format_address(organizations: list[dict]) -> None:
    for organization in organizations:
        if organization['address']:
            raw_address = organization['address']
            organization['address'] = f'Адрес: {raw_address}'


def evaluate_fraud_weight() -> None:
    organizations = Organization.objects.all()
    for organization in organizations:
        fraud_number = Bill.objects.filter(client_org=organization, fraud_score__gte=0.9).count()
        organization.fraud_weight += fraud_number
        organization.save()
