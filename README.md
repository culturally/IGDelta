# Instagram Delta

This tool uses the private Instagram API to help you identify and remove fake/bot followers from your account. **Use at your own risk.**

## Requirements
- Python 3.5+
- A secondary/aged Instagram account for scraping (to avoid limits on your main account)
- Dependencies installed via `pip install colorama requests`

## Usage

### Step 1: Scrape Followers
Use an alternate Instagram account to scrape followers from your main account.

```sh
python scrape.py
```

- Output: `followers.json`
- One aged account can scrape around **12,000** followers before rate limit.

### Step 2: Remove Duplicates
Run the script to clean duplicate entries.

```sh
python dupl.py
```

- Output: `cleaned_followers.json`
- Rename this file to `followers.json` and move it to the `blacklist/` directory.

### Step 3: Generate Blacklist
Use the `blacklist.py` script to filter out fake/bot followers based on specific criteria.

```sh
python blacklist.py
```

- Output: `blacklist.json`
- The filtering logic is based on engagement metrics like post count, follower/following ratio, etc.
- You can modify the conditions in `blacklist.py` to suit your needs:

```python
if (media_count > 1 and follower_count < 60 and following_count > 500) or \
   (media_count > 1 and follower_count < 70 and following_count > 1200) or \
   (following_count > 1100 and follower_count < 130) or \
   (media_count > 1 and follower_count < 25 and following_count > 1000) or \
   (media_count > 1 and follower_count < 50) or \
   (media_count > 11 and follower_count < 50) or \
   (media_count > 11 and follower_count < 100 and following_count > 1500) or \
   (media_count > 2 and follower_count < 40) or \
   (media_count > 1 and follower_count < 50 and following_count > 350) or \
   (follower_count < 20 and following_count > 600) or \
   (following_count > 1299 and follower_count < 50):
    # Adjust this logic as needed
```

### Step 4: Remove Fake Followers
Move `blacklist.json` to `unfollow/` and run the `main.py` script.

```sh
python main.py
```

- Login with the account where you want to remove followers.
- The script will process the removal automatically.

## Important Notes
- **Use a separate account for scraping** to avoid rate limits or bans on your main account.
- **Instagram has rate limits**, so run the scripts cautiously.

## Disclaimer
This script is provided **as-is**. The developer is not responsible for any account restrictions, bans, or actions taken by Instagram. Use with caution.

