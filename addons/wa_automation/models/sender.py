import requests
import uuid

CLIENT = 'https://www.waboxapp.com/api/send/{}?token={}&uid={}&to={}&custom_uid={}&{}={}'
TOKEN = 'd1021625324d27a35f637bd7d20437645e9432f8943a0'
SENDER = '6282221810304'

class Send_Whatsapp:
    def __init__(self, receiver, message):
        self.receiver = receiver
        self.message = message
    
    def check_number(self, phone):
        phone = phone.strip().replace("-","").replace(" ","")
        result = phone.startswith('0')
        if result:
            phone = '62' + phone[1:]
        result = phone.startswith('+62')
        if result:
            phone = phone[1:]
        return phone
    
    def send_post(self, type_message, type_post):
        phone =  self.receiver
        phone = self.check_number(phone)
        client_uuid = uuid.uuid1()
        sendwa = CLIENT.format(type_message, TOKEN, SENDER, phone,
                                    client_uuid, type_post, self.message)
        status = requests.post(sendwa)
        status_code = status.status_code
        return status_code