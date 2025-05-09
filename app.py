from flask import Flask, render_template, request
import os
import requests
from pathlib import Path
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips


app = Flask(__name__)

# Ordner sicherstellen
os.makedirs("static/audio", exist_ok=True)
os.makedirs("static/output", exist_ok=True)
os.makedirs("static/videos", exist_ok=True)

# ElevenLabs API-Daten (ersetzen!)
API_KEY = "sk_9a767c672ec7caa5ba152ad0655eb129c7ca0b47031c41ad"
VOICE_ID = "9rISulbrPx7c7FFhImRe"  # z.B. Rachel

def generate_audio(text):
    print(f"[INFO] Erzeuge Audio für: {text[:30]}...")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, headers=headers, json=data, stream=True)
    if response.status_code == 200:
        filename = text[:10].replace(" ", "_") + ".mp3"
        path = Path("static/audio") / filename
        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=128):
                f.write(chunk)
        return str(path)
    else:
        print("[ERROR] TTS fehlgeschlagen:", response.status_code)
        return None

def text_to_speech(script):
    lines = script.strip().split('\n')
    audio_files = []
    for line in lines:
        if ":" in line:
            speaker, text = line.split(":", 1)
            audio = generate_audio(text.strip())
            if audio:
                audio_files.append(audio)
    return audio_files

def create_video_with_audio(audio_files):
    print("[INFO] Erstelle Video aus Audios...")
    video = VideoFileClip("static/videos/background.mp4")
    audio_clips = [AudioFileClip(f) for f in audio_files]
    final_audio = concatenate_audioclips(audio_clips)
    final_video = video.set_audio(final_audio)
    output_path = "static/output/final_video.mp4"
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    return output_path

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        script = request.form["script"]

        print(f"[INFO] Eingabe von {name}")
        audio_files = text_to_speech(script)

        if not audio_files:
            return render_template("index.html", error="Keine Audiodateien erstellt.")

        video_path = create_video_with_audio(audio_files)
        return render_template("index.html", video_url=video_path)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
