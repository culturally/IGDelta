import requests
import json
import time
import os
import sys
from colorama import Fore, Style, init

# Initialize colorama
init()

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
{Fore.WHITE}info: {Fore.RED}One aged account should be able to scrape 12k followers.{Style.RESET_ALL}
{Fore.WHITE}file output: {Fore.RED}followers.json{Style.RESET_ALL}
==================================================
"""

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

def get_user_id(username, headers, user_data_payload):
    url = f"https://i.instagram.com/api/v1/users/{username}/usernameinfo_stream/"
    response = requests.post(url, headers=headers, data=user_data_payload)
    
    if response.status_code == 200:
        try:
            # Split the response text into separate JSON objects
            json_objects = response.text.strip().split("\n")
            for json_object in json_objects:
                parsed_object = json.loads(json_object)
                # Check if the key "user" exists in the current JSON object
                if "user" in parsed_object:
                    return parsed_object["user"].get("pk")
        except json.JSONDecodeError as e:
            print(f"{Fore.RED}JSON decode error: {e}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Error fetching user ID: {response.status_code}{Style.RESET_ALL}")
    
    return None

def fetch_followers(user_id, headers, max_id=None):
    url = f"https://i.instagram.com/api/v1/friendships/{user_id}/followers/"
    params = {"enable_groups": "true"}
    if max_id:
        params["max_id"] = max_id

    response = requests.get(url, headers=headers, params=params)
    return response

def display_header(processed_count):
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
    print(HEADER_ART)
    print(f"{Fore.WHITE}Processed Users:{Fore.RED} {processed_count}{Style.RESET_ALL}")
    print("-" * 50)

def scrape_followers():
    auth_token = login()

    # API headers with the authorization token
    common_headers = {
        "authorization": f"{auth_token}",
        "user-agent": "Instagram 361.0.0.35.82 (iPad7,11; iPadOS 15_4_1; en_US; en; scale=2.00; 2160x1620; 674117118) AppleWebKit/420+",
        "x-ig-app-id": "124024574287414",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "x-ig-device-id": "E48321D8-34B7-4C92-A41E-294F4F2C671A",
    }

    # Payload for fetching user ID
    user_data_payload = {
        "from_module": "direct_thread",
        "is_profile_prefetch": "true",
        "_uuid": "E48321D8-34B7-4C92-A41E-294F4F2C671A",  # Replace with a valid UUID if needed
        "entry_point": "profile",
        "device_id": "E48321D8-34B7-4C92-A41E-294F4F2C671A",  # Replace with a valid device ID if needed
        "_uid": "70062144220",  # Replace with the user's actual ID if available
    }

    username = input(f"{Fore.RED}Enter the Instagram username(scrape):{Fore.WHITE} {Style.RESET_ALL}").strip()
    max_id = input(f"{Fore.RED}Enter last max_id (or Press Enter to skip):{Fore.WHITE} {Style.RESET_ALL} ")
    if not max_id:
        max_id = None  
    user_id = get_user_id(username, common_headers, user_data_payload)

    if not user_id:
        print(f"{Fore.RED}Failed to fetch user ID for username: {username}{Style.RESET_ALL}")
        return

    print(f"{Fore.RED}Fetched user ID:{Fore.WHITE} {user_id}{Style.RESET_ALL}")
    data = []
    processed_count = 0

    while True:
        try:
            display_header(processed_count)
            print(f"{Fore.WHITE}Fetching followers... max_id={Fore.RED}{max_id}{Style.RESET_ALL}")

            response = fetch_followers(user_id, common_headers, max_id)
            if response.status_code != 200:
                print(f"{Fore.RED}Received bad status code: {response.status_code}{Style.RESET_ALL}")
                break

            response_data = response.json()

            # Extract data
            users = response_data.get("users", [])
            for user in users:
                data.append({
                    "id": user.get("id"),
                    "username": user.get("username"),
                })
                processed_count += 1
                display_header(processed_count)
                print(f"{Fore.WHITE}Added User: {Fore.GREEN}{user.get('username')}{Style.RESET_ALL}")

            # Update max_id for the next request
            max_id = response_data.get("next_max_id", None)

            # Stop if there's no more data to fetch
            if not max_id:
                print(f"{Fore.RED}No more data to fetch.{Style.RESET_ALL}")
                print(f"{Fore.WHITE}Last max id was {Fore.RED}{max_id}{Style.RESET_ALL}")
                break

            # Delay between requests to avoid rate-limiting
            time.sleep(0.4)
        except Exception as e:
            print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
            break

    # Save data to a JSON file
    output_file = f"{username}_followers.json"
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)


    print()
    print(f"{Fore.WHITE}Data saved to {output_file}{Style.RESET_ALL}")
    print(f"{Fore.RED}If you would like to check for duplicates or start blacklisting please rename the file to only followers.json{Style.RESET_ALL}")

# Run the scraper
if __name__ == "__main__":
    scrape_followers()
