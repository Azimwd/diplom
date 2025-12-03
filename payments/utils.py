import random
from .models import Payment

def generate_unique_invoice_id():
    while True:
        invoice_id = random.randint(100000, 999999)
        if not Payment.objects.filter(invoice_id=invoice_id).exists():
            return invoice_id