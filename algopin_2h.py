import requests
import base64
import json
from datetime import datetime, timedelta

# Client ID and secret (replace with your actual credentials)
client_id = ''
client_secret = ''

# Function to obtain the access token
def get_access_token(client_id, client_secret):
    # Base64 encode client_id and client_secret
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    # Define the token URL and headers
    url = 'https://auth.igloohome.co/oauth2/token'
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'scope': 'igloohomeapi/algopin-hourly igloohomeapi/algopin-daily igloohomeapi/algopin-permanent '
                 'igloohomeapi/algopin-onetime igloohomeapi/create-pin-bridge-proxied-job '
                 'igloohomeapi/delete-pin-bridge-proxied-job igloohomeapi/lock-bridge-proxied-job '
                 'igloohomeapi/unlock-bridge-proxied-job igloohomeapi/get-devices igloohomeapi/get-job-status'
    }

    # Request the token
    response = requests.post(url, headers=headers, data=data)

    # Check for successful response
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception(f"Failed to retrieve access token: {response.status_code} - {response.text}")

# Function to create a 2-hour Algo PIN code using the access token
def create_algo_pin_code(lock_id, access_token, start_time):
    url = f"https://api.igloodeveloper.co/igloohome/devices/{lock_id}/algopin/hourly"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Calculate end time (2 hours after the start time)
    end_time = start_time + timedelta(hours=2)

    # Define the data based on the correct API requirements
    data = {
        "startDate": start_time.strftime('%Y-%m-%dT%H:00:00+00:00'),  # Force 00:00 for minutes and seconds
        "endDate": end_time.strftime('%Y-%m-%dT%H:00:00+00:00'),
        "variance": 1,  # Choose a variance value between 1 and 3
        "accessName": "Temporary Access"  # You can modify this name as needed
    }

    # Make the POST request to create the Algo PIN code
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Handle the response
    if response.status_code == 200:
        return response.json().get('pin')
    else:
        raise Exception(f"Failed to create Algo PIN code: {response.status_code} - {response.text}")

# Main function that retrieves the token and creates the PIN code
def main():
    try:
        # Step 1: Get the access token
        access_token = get_access_token(client_id, client_secret)

        # Step 2: Validate date and time input
        while True:
            try:
                # Ask the user for the start date and time
                user_date = input("Enter the start date (YYYY-MM-DD): ")
                user_time = input("Enter the start time (HH:MM): ")

                # Combine user input into a datetime object
                start_time_str = f"{user_date} {user_time}"
                start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M')

                # Exit the loop if valid
                break
            except ValueError:
                print("Invalid date or time format. Please try again.")

        # Step 3: Create a 2-hour Algo PIN code
        lock_id = 'EK1X13bf42ea'  # Replace with your actual lock ID
        pin_code = create_algo_pin_code(lock_id, access_token, start_time)

        print(f"Successfully created a 2-hour Algo PIN code: {pin_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the main function
if __name__ == "__main__":
    main()
