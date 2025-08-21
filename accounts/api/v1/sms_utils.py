from kavenegar import KavenegarAPI, APIException, HTTPException


API_KEY = '4F36465935546338734B356B55524633773376344437547467674A6F72657447586159776E774D756146383D'
SENDER = '2000660110'
def send_sms(mobile, message, test=True):
    if test:
        print(f"[TEST MODE] SMS to {mobile}: {message}")
        return True
    
    try:
        api = KavenegarAPI(API_KEY)
        params = {
            'sender': SENDER,
            'receptor': mobile,
            'message': message
        }
        response = api.sms_send(params)
        print("SMS Response:", response)
        return True
    
    except (APIException, HTTPException) as e:
        print("SMS failed:", e)
        return False