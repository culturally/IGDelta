import json

# Load the JSON file
with open('followers.json', 'r') as file:
    followers_data = json.load(file)

# Create a set to track unique user ids and usernames
seen_ids = set()
seen_usernames = set()

# List to store the unique followers
unique_followers = []

# Iterate through the list and add only unique entries
for follower in followers_data:
    if follower['id'] not in seen_ids and follower['username'] not in seen_usernames:
        unique_followers.append(follower)
        seen_ids.add(follower['id'])
        seen_usernames.add(follower['username'])

# Save the unique followers back into the file
with open('followers_cleaned.json', 'w') as file:
    json.dump(unique_followers, file, indent=4)

print("Duplicates removed and data saved to 'followers_cleaned.json'.")
