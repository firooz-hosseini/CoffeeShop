import os
from kavenegar import KavenegarAPI, APIException, HTTPException

KAVENEGAR_API_KEY = os.environ.get("KAVENEGAR_API_KEY")

def send_sms(mobile, message, test=True):
    if test:
        print(f"[TEST MODE] SMS to {mobile}: {message}")
        return True
    
    try:
        api = KavenegarAPI(KAVENEGAR_API_KEY)
        response = api.sms_send(
            sender="2000660110",
            receptor=mobile,
            message=message
        )
        print(response)
        return True
    except (APIException, HTTPException) as e:
        print("SMS failed:", e)
        return False