import requests


def ping_net():
    try:
        code = requests.get("https://google.com")

        print(code.status_code)

        if code.status_code == 200:
            return True

    except:
        return False

