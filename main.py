import os
import requests
from datetime import datetime
from termcolor import colored
from session import sessions


def get_data(session_data, type: str = "me"):
    url = (
        "https://nanogames.io/api/user/get/"
        if type == "me"
        else "https://nanogames.io/api/game/support/click-roll/"
    )

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Host": "nanogames.io",
        "Referer": (
            "https://nanogames.io/"
            if type == "me"
            else "https://nanogames.io/api/game/support/click-roll/"
        ),
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
    }

    cookies = {
        "__cf_bm": session_data["__cf_bm"],
        "cf_clearance": session_data["cf_clearance"],
        "JSESSIONID": session_data["JSESSIONID"],
        "SESSION": session_data["SESSION"],
    }

    res = requests.get(url=url, headers=headers, cookies=cookies)
    res_json = res.json()

    return (
        {
            "email": (
                res_json["data"]["email"] if res_json["data"] is not None else None
            ),
            "viplevel": (
                res_json["data"]["vipLevel"] if res_json["data"] is not None else None
            ),
            "roll": (
                res_json["data"]["roll"]
                if res_json["data"] is not None and "roll" in res_json["data"]
                else 0
            ),
        }
        if res.status_code == 200
        else {
            "msg": print(f"Error Occured:\nCode: {res.status_code}\nMessage: {res}"),
            "email": None,
            "viplevel": None,
            "roll": 0,
        }
    )


### Variables ###
results = []

for i, session in enumerate(sessions):
    my_details = get_data(session)
    email, viplevel, roll = (
        my_details["email"],
        my_details["viplevel"],
        get_data(session)["roll"],
    )
    results.append((roll, email, viplevel))

    print(
        colored(f"{i + 1}. ", "light_magenta", attrs=["bold"]),
        colored(f"Rollback: {roll} -", "blue", attrs=["bold"]),
        colored(f"Email: {email} -", "green"),
        colored(f"VipLevel: {viplevel}", "yellow"),
    )


results.sort(key=lambda x: x[0], reverse=True)
os.makedirs("results", exist_ok=True)
with open(f"results/{datetime.now().strftime("%Y-%m-%d")}.txt", "a") as file:
    for roll, email, viplevel in results:
        file.write(f"Rollback: {roll} - Email: {email} - VipLevel: {viplevel}\n")
