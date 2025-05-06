import requests

api_key = "DEIN_API_KEY"
voice_id = "9rISulbrPx7c7FFhImRe"
text = "Hallo! Ich bin eine KI-Stimme von ElevenLabs."

url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

headers = {
    "xi-api-key": api_key,
    "Content-Type": "application/json"
}

payload = {
    "text": text,
    "model_id": "eleven_multilingual_v2",  # oder je nach Voice auch "eleven_monolingual_v1"
    "voice_settings": {
        "stability": 0.75,
        "similarity_boost": 0.75
    }
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    with open("output.mp3", "wb") as f:
        f.write(response.content)
    print("Audio gespeichert als output.mp3 ✅")
else:
    print("Fehler beim Generieren des Audios:", response.status_code)
    print(response.text)
