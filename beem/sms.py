import json
import requests



def phone_repr(phone):
    new_number = ""
    if phone != "":
        for i in range(phone.__len__()):
            if i == 0:
                pass
            else:
                new_number = new_number + phone[i]
        number = "255" + new_number
        public_number = number
        return public_number


def send_sms(phone, name):
    URL = 'https://apisms.beem.africa/v1/send'
    content_type = 'application/json'
    source_addr = 'INVENTORY'
    secrete_key = "YmE1NmRmNzVmY2JhN2RjYmI0ZGU1OTJlMzFlNWU4MDdhYzQ2MWNlNWVmZDVkNWFkNzYxOWUyNjRmNGNmYmNiNQ=="
    api_key = 'b7a0b864387611b6'
    phonee = phone_repr(phone)
    apikey_and_apisecret = api_key + ':' + secrete_key

    first_request = requests.post(url=URL, data=json.dumps({
        'source_addr': 'INVENTORY',
        'schedule_time': '',
        'encoding': '0',
        'message': f"{name}",
        'recipients': [
            {
                'recipient_id': 1,
                'dest_addr': phonee,
            }
        ],
    }),

                                  headers={
                                      'Content-Type': content_type,
                                      'Authorization': 'Basic ' + api_key + ':' + secrete_key,
                                  },
                                  auth=(api_key, secrete_key), verify=False)

    print(first_request.status_code)
    print(first_request.json())
    return (first_request.json())


#send_sms('0715700411', 'Albendazol', '6754764799',)
