from typing import Union

import requests

from requests.exceptions import HTTPError, RequestException

import os

API_BASE = "https://discord.com/api/v10"


def send_request(method: str, endpoint: str, data: dict = None, headers=None) -> Union[list, dict, Exception]:
    if headers is None:
        headers = {"Authorization": f"Bot {os.environ['TOKEN']}"}
    try:
        res = requests.request(method, f"{API_BASE}/{endpoint}", headers=headers, json=data)
        res.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)
        data = res.json()
        if isinstance(data, dict):
            if data.get("error"):
                raise HTTPError(data["error"])
        return data
    except RequestException as e:
        return {"error": f"Request exception occurred: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}


def get_guild(guild_id: int) -> dict:
    data = send_request("GET", f"guilds/{guild_id}")
    return data


def getUserID(accessToken: str):
    print(accessToken)
    res = send_request("GET", f"users/@me", headers={"Authorization": f"Bearer {accessToken}"})
    return res['id']

def getRoles(guild_id: int):
    data = send_request("GET", f"guilds/{guild_id}/roles")
    return data

def getChannels(guild_id: int):
    data = send_request("GET", f"guilds/{guild_id}/channels")
    return data

def checkPermissions(user: dict, guild_id: int) -> bool:
    access_token = user['access_token']
    guild = get_guild(guild_id)
    user_id = getUserID(access_token)
    member = send_request("GET", f"guilds/{guild_id}/members/{user_id}")
    member_roles = member['roles']
    guild_roles = getRoles(guild_id)


    if guild['owner_id'] == user_id:
        return True

    for role in guild_roles:
        if role['id'] in member_roles:
            if role['permissions'] & 0x8 == 0x8:
                return True
