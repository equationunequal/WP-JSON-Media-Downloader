# Author:   Christian Wiegman | equationunequal
# Website:  http://www.newskin.nl
# Purpose:  Download all media files from a WordPress website using the wp-json API
# License:  http://unlicense.org

# Imports
import requests
import os

# Set the URL of the WordPress site
site_url = input("Enter the URL of the WordPress site: ")

# Create media directory if it does not exist
if not os.path.exists('media'):
   os.makedirs('media')

# Add http:// if needed
if site_url.startswith("http://") == False and site_url.startswith("https://") == False:
    site_url = "http://" + site_url

print("Scanning site: " + site_url)

end_reached = False
page_number = 1

while end_reached == False:
    # Make a GET request to retrieve a list with all media files (maximum 100 per page)
    wp_response = requests.get(f"{site_url}/wp-json/wp/v2/media/?per_page=100&page=" + str(page_number)).json()

    print("Downloading files from page " + str(page_number))

    # Check for page without media files
    if isinstance(wp_response, dict) and wp_response["code"] == "rest_post_invalid_page_number":
        end_reached = True
        print("Reached the end.")
        break
    else:
        # Loop through each media file and download it
        for media in wp_response:
            media_url = media["source_url"]
            media_file_name = os.path.basename(media_url)
            media_file_path = f"media/{media_file_name}"
            media_file = requests.get(media_url)
            
            # Save the media file in the media directory
            with open(media_file_path, "wb") as f:
                f.write(media_file.content)

    page_number += 1

# Version History
# 2024-02-10: 1.0
# 2024-02-11: 1.1 Add http:// if needed, create media directory if not present