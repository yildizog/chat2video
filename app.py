from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Pfade für Uploads vorbereiten
UPLOAD_FOLDER = "static/images"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Hier werden später die Formdaten verarbeitet
        pass

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

import requests
import os
from pathlib import Path

# Deine API-Key und Voice-ID
API_KEY = 'Dein_ElevenLabs_API_Key'  # Ersetze durch deinen echten API-Key
VOICE_ID = '9rISulbrPx7c7FFhImRe'  # Ersetze durch deine tatsächliche Voice-ID (z.B. Rachel)

# Text in Audio umwandeln
def text_to_speech(script):
    # Die Nachrichten in Personen unterteilen
    messages = script.split('\n')
    
    audio_files = []
    for message in messages:
        if message.startswith("Person1:"):
            # Text für Person1
            text = message.replace("Person1:", "").strip()
            audio_file = generate_audio(text)
            audio_files.append(audio_file)
        elif message.startswith("Person2:"):
            # Text für Person2
            text = message.replace("Person2:", "").strip()
            audio_file = generate_audio(text)
            audio_files.append(audio_file)
    
    return audio_files

# Anfrage an ElevenLabs API, um Text in Audio zu verwandeln
def generate_audio(text):
    url = f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream'
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'text': text,
        'voice_settings': {
            'stability': 0.5,
            'similarity_boost': 0.5
        }
    }
    
    response = requests.post(url, headers=headers, json=data, stream=True)
    
    if response.status_code == 200:
        # Audio-Daten in einer Datei speichern
        audio_path = Path("static/audio") / f"{text[:10]}.mp3"  # Dateiname basierend auf Text
        with open(audio_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=128):
                f.write(chunk)
        return audio_path
    else:
        print(f"Fehler bei der TTS-Anfrage: {response.status_code}")
        return None

from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

# Funktion zum Kombinieren von Video und Audio
def create_video_with_audio(audio_files, background_video_path='static/videos/background.mp4'):
    # Lade das Hintergrundvideo
    video = VideoFileClip(background_video_path)
    
    audio_clips = []
    
    # Füge für jede Audiodatei eine Audio-Clip hinzu
    for audio_file in audio_files:
        audio_clip = AudioFileClip(audio_file)
        audio_clips.append(audio_clip)
    
    # Kombiniere die Audiodateien
    final_audio = concatenate_audioclips(audio_clips)
    
    # Wechsle die Audioquelle des Hintergrundvideos
    video = video.set_audio(final_audio)
    
    # Exportiere das fertige Video
    output_video_path = 'static/output/final_video.mp4'
    video.write_videofile(output_video_path, codec='libx264', audio_codec='aac')
    
    return output_video_path


from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

# Sicherstellen, dass die entsprechenden Ordner existieren
os.makedirs('static/audio', exist_ok=True)
os.makedirs('static/videos', exist_ok=True)
os.makedirs('static/output', exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        profile_picture = request.files['profile_picture']
        name = request.form['name']
        script = request.form['script']
        
        # Script in Audio umwandeln
        audio_files = text_to_speech(script)
        
        # Kombiniere Audio mit Hintergrundvideo
        video_path = create_video_with_audio(audio_files)
        
        # Zeige das Video auf der Webseite an
        return render_template('index.html', video_url=video_path)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
