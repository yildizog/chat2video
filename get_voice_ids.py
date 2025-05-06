import requests

api_key = "DEIN_API_KEY"  # Ersetze das durch deinen echten ElevenLabs API Key
url = "https://api.elevenlabs.io/v1/voices"

headers = {
    "xi-api-key": api_key
}

response = requests.get(url, headers=headers)
print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    for voice in data.get("voices", []):
        print(f"Voice: {voice['name']}, ID: {voice['voice_id']}")
else:
    print(f"Fehler: {response.text}")
