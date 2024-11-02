import requests
from termcolor import colored
import time

url = "https://api.mail.tm"
domain = requests.get(url=url + "/domains").json()["hydra:member"][0]["domain"]
mail = []
num = 600


def create_account(index, domain):
    address = f"larry{index}@{domain}"
    password = "Milkymagic@0123"
    try:
        response = requests.post(
            url=url + "/accounts",
            json={"address": address, "password": password},
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        reg = response.json()
        return reg["address"]
    except requests.exceptions.HTTPError as http_err:
        print(colored(f"HTTP error occurred: {http_err}", "red", attrs=["bold"]))
    except Exception as e:
        print(colored(f"Other error occurred: {e}", "red", attrs=["bold"]))
    return None


for i in range(1000):
    backoff_time = 1
    while True:
        email = create_account(num, domain)
        if email:
            mail.append(email)
            print(colored(f"Email has been created: {email}", "green", attrs=["bold"]))
            break
        else:
            print(
                colored(
                    f"Failed to create email for index {num}, retrying in {backoff_time} seconds...",
                    "red",
                    attrs=["bold"],
                )
            )
            time.sleep(backoff_time)
            backoff_time *= 2

    num = num + 1
    time.sleep(3)

print(mail)
