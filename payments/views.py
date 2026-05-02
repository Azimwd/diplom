import hashlib
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from .models import Payment
from .utils import generate_unique_invoice_id
from rest_framework.permissions import IsAuthenticated
import urllib.parse
from django.contrib.auth import get_user_model
from rest_framework.views import APIView, Response
from rest_framework import status

User = get_user_model()

class GetInvoiceUrlView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        invoice_id = request.data.get("invoice_id")

        try:
            payment = Payment.objects.get(invoice_id=invoice_id)
        except Payment.DoesNotExist:
            return JsonResponse({"error": "Invoice not found"}, status=404)
        
        if payment.is_paid:
            return JsonResponse({"error": "Этот счёт уже был оплачен"}, status=400)
              
        login = settings.ROBOKASSA_LOGIN
        password1 = settings.ROBOKASSA_PASSWORD1
        amount = payment.amount
        desc = f"Оплата заказа №{payment.invoice_id}"
        desc_encoded = urllib.parse.quote(desc)

        signature = f"{login}:{amount:.2f}:{payment.invoice_id}:{password1}"
        signature_hash = hashlib.md5(signature.encode('utf-8')).hexdigest()

        url = (
            f"https://auth.robokassa.kz/Merchant/Index.aspx?"
            f"MerchantLogin={login}&OutSum={amount:.2f}&InvId={payment.invoice_id}"
            f"&Description={desc_encoded}&SignatureValue={signature_hash}"
            f"&Email={request.user.email}&IsTest=1"
        )

        return JsonResponse({"url": url})


from subscriptions.models import Subscription
from django.utils.timezone import now, timedelta

class RobokassaResultView(APIView):
    def post(self, request):
        out_sum = request.POST.get('OutSum')
        inv_id = request.POST.get('InvId')
        received_sig = request.POST.get('SignatureValue', '').upper()

        if not all([out_sum, inv_id, received_sig]):
            return HttpResponse("error: missing data")

        password2 = settings.ROBOKASSA_PASSWORD2
        signature_str = f"{out_sum}:{inv_id}:{password2}"
        expected_sig = hashlib.md5(signature_str.encode('utf-8')).hexdigest().upper()

        if received_sig != expected_sig:
            return HttpResponse("error: signature mismatch")

        try:
            inv_id = int(inv_id)
            payment = Payment.objects.get(invoice_id=inv_id)
        except (ValueError, Payment.DoesNotExist):
            return HttpResponse("error: no such order")

        if not payment.is_paid:
            payment.is_paid = True
            payment.save()

            duration_map = {
                "1m": timedelta(minutes=1),
                "6m": timedelta(days=180),
                "1y": timedelta(days=365),
            }
            plan = payment.plan
            if plan in duration_map:
                Subscription.objects.create(
                    user=payment.payer,
                    plan=plan,
                    end_date=now() + duration_map[plan]
                )

        return HttpResponse(f"OK{inv_id}")

class CreateSubscriptionInvoiceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        plan = request.data.get("plan")
        amount_map = {
            "1m": 10000,
            "6m": 50000,
            "1y": 90000,
        }
        
        if plan not in amount_map:
            return JsonResponse({"error": "Invalid plan"}, status=400)

        payment = Payment.objects.create(
            payer=request.user,
            receiver=None,
            amount=amount_map[plan],
            invoice_id=generate_unique_invoice_id(),
            purpose="subscription",
            plan=plan
        )

        response = Response({
            "invoice_id": payment.invoice_id,
            "plan": plan,
            "amount": payment.amount,
            "message": "Подписку создана"
        }, status=status.HTTP_200_OK)

        return response



class RobokassaSuccessView(APIView):
    def get(self, request):
        inv_id = request.GET.get("InvId")

        if not inv_id:
            return HttpResponse("inv_id! Оплата прошла успешно.")

        try:
            payment = Payment.objects.get(invoice_id=inv_id)
        except Payment.DoesNotExist:
            return HttpResponse("DoesNotExist! Оплата прошла успешно.")

        return HttpResponse("Спасибо! Оплата прошла успешно.")



class RobokassaFailView(APIView):
    def get(self, request):
        return HttpResponse("Оплата не удалась. Попробуйте снова.")
    

