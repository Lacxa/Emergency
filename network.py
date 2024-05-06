import requests


def ping_net():
    try:
        code = requests.get("https://console.firebase.google.com/project/medics-inventorry/database/medics-inventorry-default-rtdb/data")

        print(code.status_code)

        if code.status_code == 200:
            return True

    except:
        return False

