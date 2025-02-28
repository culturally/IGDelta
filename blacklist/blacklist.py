import json
import requests
import time
from colorama import Fore, Style, init
import os
import sys

init()

HEADER_ART = f"""
{Fore.RED}▄█   ▄▀  ██▄   ▄███▄   █      ▄▄▄▄▀ ██   {Style.RESET_ALL}
{Fore.RED}██ ▄▀    █  █  █▀   ▀  █   ▀▀▀ █    █ █  {Style.RESET_ALL}
{Fore.RED}██ █ ▀▄  █   █ ██▄▄    █       █    █▄▄█ {Style.RESET_ALL}
{Fore.RED}▐█ █   █ █  █  █▄   ▄▀ ███▄   █     █  █ {Style.RESET_ALL}
{Fore.RED} ▐  ███  ███▀  ▀███▀       ▀ ▀         █ {Style.RESET_ALL}
{Fore.RED}                                      █  {Style.RESET_ALL}
{Fore.RED}                                     ▀   {Style.RESET_ALL}

{Fore.WHITE}powered by {Fore.RED}yin.sh{Style.RESET_ALL}  

{Fore.WHITE}version: {Fore.RED}blacklist{Style.RESET_ALL}
{Fore.WHITE}file input: {Fore.RED}followers.json{Style.RESET_ALL}
{Fore.WHITE}file output: {Fore.RED}blacklist.json{Style.RESET_ALL}
==================================================
"""

# Load followers data from followers.json
def load_followers():
    with open('followers.json', 'r') as file:
        return json.load(file)

# Save blacklisted users to blacklist.json without overwriting existing data
def save_blacklist(user):
    try:
        with open('blacklist.json', 'r') as file:
            existing_blacklist = json.load(file)
    except FileNotFoundError:
        existing_blacklist = []

    if user['id'] not in {u['id'] for u in existing_blacklist}:
        existing_blacklist.append(user)
        with open('blacklist.json', 'w') as file:
            json.dump(existing_blacklist, file, indent=4)

# Fetch user info by ID from Instagram API
def get_user_info(user_id, authorization_token):
    url = f"https://i.instagram.com/api/v1/users/{user_id}/info_stream/"
    headers = {
        "Authorization": authorization_token,
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Instagram 361.0.0.35.82 (iPad7,11; iPadOS 15_4_1; en_US; en; scale=2.00; 2160x1620; 674117118) AppleWebKit/420+",
        "x-ig-app-id": "124024574287414",
        "x-ig-device-id": "1E98C19B-BF8F-4CC2-BA69-059B253A4863",
        "ig-u-ds-user-id": "54101392648"
    }

    data = {"from_module":"feed_timeline","is_profile_prefetch":"true","_uuid":"1E98C19B-BF8F-4CC2-BA69-059B253A4863","entry_point":"profile","device_id":"1E98C19B-BF8F-4CC2-BA69-059B253A4863","_uid":"54101392648"}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        return None, response.status_code
    return response.json(), 200

# Login to Instagram and retrieve authorization token
def login():
    login_url = "https://i.instagram.com/api/v1/accounts/login/"
    os.system('cls' if os.name == 'nt' else 'clear')
    print(HEADER_ART)
    username = input(f"{Fore.RED}Enter your Instagram username:{Fore.WHITE} @{Style.RESET_ALL}")
    password = input(f"{Fore.RED}Enter your Instagram password:{Fore.WHITE} {Style.RESET_ALL}")
    login_data = {
        "phone_id": "E48321D8-34B7-4C92-A41E-294F4F2C671A",
        "reg_login": "0",
        "device_id": "E48321D8-34B7-4C92-A41E-294F4F2C671A",
        "has_seen_aart_on": "1",
        "att_permission_status": "0",
        "username": username,
        "login_attempt_count": "0",
        "enc_password": f"#PWD_INSTAGRAM:0:0:{password}"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent": "Instagram 361.0.0.35.82 (iPad7,11; iPadOS 15_4_1; en_US; en; scale=2.00; 2160x1620; 674117118) AppleWebKit/420+",
        "accept-language": "en-US;q=1.0",
        "accept-encoding": "gzip, deflate",
    }
    response = requests.post(login_url, headers=headers, data=login_data)

    if response.status_code != 200:
        print(f"{Fore.RED}Failed to log in. HTTP Status Code: {response.status_code}{Style.RESET_ALL}")
        sys.exit("Exiting script")

    response_data = response.json()
    if response_data.get("status") != "ok" or "logged_in_user" not in response_data:
        print(f"{Fore.RED}Login failed. Check your credentials or account status.{Style.RESET_ALL}")
        sys.exit("Exiting script")

    print(f"{Fore.GREEN}Login successful as {response_data['logged_in_user']['username']}.{Style.RESET_ALL}")

    # Extract Authorization token from response headers
    authorization_token = response.headers.get("ig-set-authorization", "")
    if not authorization_token:
        print(f"{Fore.RED}Authorization token not found in response headers.{Style.RESET_ALL}")
        sys.exit("Exiting script")

    return authorization_token
    
    
# Process users and blacklist based on conditions
def process_users():
    followers = load_followers()
    processed_count = 0
    blacklisted_count = 0
    blacklist = []

    # Login and get token
    authorization_token = login()

    # Prompt for custom delay
    try:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
        print(HEADER_ART)
        print()
        print()
        custom_delay = float(input(f"{Fore.RED}Enter custom delay in seconds:{Fore.WHITE} {Style.RESET_ALL}"))
    except ValueError:
        print(f"{Fore.RED}Invalid input. Using default delay of 1 second.{Style.RESET_ALL}")
        custom_delay = 1.0


    for user in followers:
        processed_count += 1
        user_id = user['id']
        username = user['username']
        
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
        
        # Display Header
        print(HEADER_ART)
        
        # Display Process Stats
        print(f"{Fore.WHITE}Processed Users:{Fore.RED} {processed_count}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Blacklisted Users:{Fore.RED} {blacklisted_count}{Style.RESET_ALL}")
        print()
        print('-' * 50)

        user_info, status_code = get_user_info(user_id, authorization_token)
        if not user_info:
            print(f"{Fore.RED}Error fetching data for UserID: {user_id} (Status Code: {status_code}){Style.RESET_ALL}")
            print(f"{Fore.RED}Most likely rate limit please use different account or wait")
            sys.exit("Exiting script")

        user_data = user_info.get('user', {})
        following_count = user_data.get('following_count', 0)
        follower_count = user_data.get('follower_count', 0)
        media_count = user_data.get('media_count', 0)

        if (media_count > 1 and follower_count < 60 and following_count > 500) or (media_count > 1 and follower_count < 70 and following_count > 1200) or (following_count > 1100 and follower_count < 130) or (media_count > 1 and follower_count < 25 and following_count > 1000) or (media_count > 1 and follower_count < 50) or (media_count > 11 and follower_count < 50) or (media_count > 11 and follower_count < 100 and following_count > 1500) or (media_count > 2 and follower_count < 40) or (media_count > 1 and follower_count < 50 and following_count > 350) or (follower_count < 20 and following_count > 600) or (following_count > 1299 and follower_count < 50): #adjust this to ur needs
            blacklisted_count += 1
            blacklisted_user = {
                'id': user_id,
                'username': username,
                'following_count': following_count,
                'follower_count': follower_count,
                'media_count': media_count
            }
            save_blacklist(blacklisted_user)
            blacklist.append(blacklisted_user)
            print(f"{Fore.RED}Blacklisted: UserID = {user_id}, Username = {username}{Style.RESET_ALL}")
        else:
            print(f"{Fore.WHITE}Checked: UserID = {user_id}, Username = {username}{Style.RESET_ALL}")

        time.sleep(custom_delay)  

if __name__ == "__main__":
    process_users()
