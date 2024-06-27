def get_open_msg(token:str, status: str):
    return {
    "op": 2,
    "d": {
        "token": token,
        "properties": {
            "$os": "Windows 10",
            "$browser": "Google Chrome",
            "$device": "Windows",
        },
        "presence": {
            "status": status,
            "afk": False
        }
    }
}


def get_ping_msg(status: str):
    return {
    "op": 3,
    "d": {
        "since": 0,
        "activities": [
            {
                "type": 4,
                "state": "PyCharm",
                "name": "Custom Status",
                "id": "custom"
            }
        ],
        "status": status,
        "afk": False
    }
}