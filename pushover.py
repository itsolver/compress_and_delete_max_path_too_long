import requests

def send_pushover(text, user, api):
    """Send a message via Pushover."""
    try:
        payload = {"message": text, "user": user, "token": api}
        print(f"Payload: {payload}")
        r = requests.post('https://api.pushover.net/1/messages.json',
                          data=payload, headers={'User-Agent': 'Python'}, timeout=10)
        print(f"Response: {r.content}")
        
        # Check if the request was successful
        if r.status_code == 200:
            print("Notification sent successfully.")
        else:
            print(f"Failed to send notification. Status code: {r.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending notification: {e}")

    return r