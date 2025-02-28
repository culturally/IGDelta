import json
import requests
import time
import os
import sys
from colorama import Fore, Style, init

init()

# API Endpoint
API_URL = "https://i.instagram.com/api/v1/friendships/remove_follower/"

# Banner for UI
HEADER_ART = f"""
{Fore.RED}▄█   ▄▀  ██▄   ▄███▄   █      ▄▄▄▄▀ ██   {Style.RESET_ALL}
{Fore.RED}██ ▄▀    █  █  █▀   ▀  █   ▀▀▀ █    █ █  {Style.RESET_ALL}
{Fore.RED}██ █ ▀▄  █   █ ██▄▄    █       █    █▄▄█ {Style.RESET_ALL}
{Fore.RED}▐█ █   █ █  █  █▄   ▄▀ ███▄   █     █  █ {Style.RESET_ALL}
{Fore.RED} ▐  ███  ███▀  ▀███▀       ▀ ▀         █ {Style.RESET_ALL}
{Fore.RED}                                      █  {Style.RESET_ALL}
{Fore.RED}                                     ▀   {Style.RESET_ALL}

{Fore.WHITE}powered by {Fore.RED}yin.sh{Style.RESET_ALL}  

{Fore.WHITE}version: {Fore.RED}scrape{Style.RESET_ALL}
{Fore.WHITE}info: {Fore.RED}Login with the account you want to remove followers on.{Style.RESET_ALL}
{Fore.WHITE}file input: {Fore.RED}blacklist.json{Style.RESET_ALL}
==================================================
"""

# Define the login function to retrieve the authorization token
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
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')

    # Extract Authorization token from response headers
    authorization_token = response.headers.get("ig-set-authorization", "")
    if not authorization_token:
        print(f"{Fore.RED}Authorization token not found in response headers.{Style.RESET_ALL}")
        sys.exit("Exiting script")

    return authorization_token


# Function to load the blacklist
def load_blacklist(file_path="blacklist.json"):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: The file {file_path} was not found.{Style.RESET_ALL}")
        return []
    except json.JSONDecodeError:
        print(f"{Fore.RED}Error: The file {file_path} contains invalid JSON.{Style.RESET_ALL}")
        return []


# Function to unfollow users
def unfollow_user(user_id, headers):
    api_url = "https://i.instagram.com/api/v1/friendships/remove_follower/"
    post_data = {
        "_uuid": "D29371C7-7766-49C0-B438-196D2A073266",
        "_uid": "70062144220",
        "device_id": "D29371C7-7766-49C0-B438-196D2A073266",
        "container_module": "self_followers",
        "include_follow_friction_check": "1",
        "user_id": user_id
    }

    try:
        response = requests.post(api_url + user_id + "/", headers=headers, json=post_data)
        print(response.text)
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "ok":
                print(f"{Fore.GREEN}Removed follower user ID: {user_id}{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.YELLOW}Failed to remove user ID: {user_id} - {result}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}HTTP Error for user ID: {user_id} - Status Code: {response.status_code}{Style.RESET_ALL}")
            sys.exit()
    except Exception as e:
        print(f"{Fore.RED}Exception occurred while unfollowing user ID: {user_id} - {e}{Style.RESET_ALL}")
    return False


# Main function
def main():
    authorization_token = login()  # Get the authorization token

    # Define headers **after** login
    HEADERS = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent": "Instagram 361.0.0.35.82 (iPad7,11; iPadOS 15_4_1; en_US; en; scale=2.00; 2160x1620; 674117118) AppleWebKit/420+",
        "accept-language": "en-US;q=1.0",
        "accept-encoding": "gzip, deflate",
        "authorization": authorization_token  # Insert the token
    }

    blacklist = load_blacklist()
    if not blacklist:
        print(f"{Fore.YELLOW}No users found in the blacklist.{Style.RESET_ALL}")
        return

    for user in blacklist:
        user_id = user.get("id")
        if not user_id:
            print(f"{Fore.RED}Invalid entry in blacklist: missing 'id' key.{Style.RESET_ALL}")
            continue

        print(f"{Fore.BLUE}Attempting to unfollow user ID: {user_id}{Style.RESET_ALL}")
        unfollow_user(user_id, HEADERS)
        time.sleep(2.1)  # Prevent rate limits

if __name__ == "__main__":
    main()
