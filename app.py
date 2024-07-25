from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        transcript = request.form['transcript']
        processed_transcript = process_transcript(transcript)
        return render_template('index.html', original=transcript, processed=processed_transcript)
    return render_template('index.html')

def process_transcript(transcript):
    headers = {
        "authorization": ASSEMBLYAI_API_KEY,
        "content-type": "application/json"
    }

    # Punctuation and Casing
    response = requests.post(
        "https://api.assemblyai.com/v2/punctuate",
        json={"text": transcript},
        headers=headers
    )
    response_data = response.json()
    punctuated_text = response_data.get('text', '')

    # Inverse Text Normalization (ITN)
    response = requests.post(
        "https://api.assemblyai.com/v2/itn",
        json={"text": punctuated_text},
        headers=headers
    )
    response_data = response.json()
    itn_text = response_data.get('text', '')

    return itn_text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)