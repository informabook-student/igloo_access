import requests
import base64
import json
from datetime import datetime, timedelta

# Client ID and secret (replace with your actual credentials)
client_id = ''
client_secret = ''

# Function to obtain the access token
def get_access_token(client_id, client_secret):
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    url = 'https://auth.igloohome.co/oauth2/token'
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'scope': 'igloohomeapi/create-pin-bridge-proxied-job igloohomeapi/get-devices igloohomeapi/lock-bridge-proxied-job'
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception(f"Failed to retrieve access token: {response.status_code} - {response.text}")

# Function to create a PIN via Bridge using the access token
def create_bridge_random_pin(lock_id, bridge_id, access_token, custom_pin, start_time):
    url = f"https://api.igloodeveloper.co/igloohome/devices/{lock_id}/jobs/bridges/{bridge_id}"

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    end_time = start_time + timedelta(hours=2)

    # Convert start_time and end_time to the required ISO 8601 format
    start_time_iso = start_time.strftime('%Y-%m-%dT%H:%M:%S+00:00')
    print(start_time)
    end_time_iso = end_time.strftime('%Y-%m-%dT%H:%M:%S+00:00')

    print(start_time_iso)

    # Define the data for the Bridge-proxied job to create the PIN  ww
    data = {
        "jobType": 4,  # Based on the image for duration PIN
        "jobData": {
            "pin": custom_pin,  # User-imposed custom PIN
            "pinType": 4,  # From the payload format, indicating duration PIN
            "startDate": start_time_iso,
            "endDate": end_time_iso,
            "accessName": 'test'
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to create Bridge PIN: {response.status_code} - {response.text}")

# Main function that retrieves the token and creates the random PIN code via the bridge
def main():
    try:
        access_token = get_access_token(client_id, client_secret)

        # Validate date and time input
        while True:
            try:
                user_date = input("Enter the start date (YYYY-MM-DD): ")
                user_time = input("Enter the start time (HH:MM): ")

                start_time_str = f"{user_date} {user_time}"
                start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M')

                break
            except ValueError:
                print("Invalid date or time format. Please try again.")

        custom_pin = str(input("Enter a custom PIN code (e.g., 123456): "))

        lock_id = 'OE1X12d87626'  # Replace with your actual lock ID
        bridge_id = 'EB1X04879082'  # Replace with your actual bridge ID
        response_data = create_bridge_random_pin(lock_id, bridge_id, access_token, custom_pin, start_time)

        print(f"Successfully created a random PIN via Bridge: {response_data}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
