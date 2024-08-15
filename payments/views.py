from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

@csrf_exempt
def initiate_payment(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        amount = request.POST.get('amount')
        
        # Dummy M-Pesa API call
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer <access_token>"}
        payload = {
            "BusinessShortCode": "<business_shortcode>",
            "Password": "<password>",
            "Timestamp": "<timestamp>",
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": "<business_shortcode>",
            "PhoneNumber": phone_number,
            "CallBackURL": "https://yourwebsite.com/payments/callback/",
            "AccountReference": "Community Platform",
            "TransactionDesc": "Payment for subscription"
        }
        
        response = requests.post(api_url, json=payload, headers=headers)
        
        return JsonResponse(response.json())

    return JsonResponse({"error": "Invalid request method"})