# spotify_auth.py

import requests
import base64

# Replace these with your actual Client ID and Client Secret
CLIENT_ID = "936c9d527fcd40c3ad06da6c4962d576"
CLIENT_SECRET = "fd160335bb904c6894e8d5b3f91a9f39"

def get_access_token():
    auth_url = "https://accounts.spotify.com/api/token"
    
    # Encode credentials in base64
    client_creds = f"{CLIENT_ID}:{CLIENT_SECRET}"
    client_creds_b64 = base64.b64encode(client_creds.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {client_creds_b64}"
    }
    
    data = {
        "grant_type": "client_credentials"
    }
    
    response = requests.post(auth_url, headers=headers, data=data)
    token_data = response.json()
    
    if "access_token" in token_data:
        return token_data["access_token"]
    else:
        raise Exception(f"Could not authenticate: {token_data}")

# Test it:
if __name__ == "__main__":
    token = get_access_token()
    print("Access token:", token)
