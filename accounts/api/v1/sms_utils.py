from kavenegar import KavenegarAPI, APIException, HTTPException

def send_sms(mobile, message, test=True):
    if test:
        print(f"[TEST MODE] SMS to {mobile}: {message}")
        return True
    
    try:
        api = KavenegarAPI('4F36465935546338734B356B55524633773376344437547467674A6F72657447586159776E774D756146383D')
        response = api.sms_send({
            'receptor': mobile,
            'message': message,
            'sender': '2000660110'
        })
        print(response)
        return True
    except (APIException, HTTPException) as e:
        print("SMS failed:", e)
        return False