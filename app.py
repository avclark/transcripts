from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')

# Print the API key to verify it's being read correctly (remove this in production)
print(f"AssemblyAI API Key: {ASSEMBLYAI_API_KEY}")

@app.route('/debug-env')
def debug_env():
    return f"ASSEMBLYAI_API_KEY: {ASSEMBLYAI_API_KEY}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        transcript = request.form['transcript']
        try:
            processed_transcript = process_transcript(transcript)
        except Exception as e:
            # Print the error message to the console
            print(f"Error processing transcript: {e}")
            return render_template('index.html', original=transcript, processed="Error processing transcript.")
        return render_template('index.html', original=transcript, processed=processed_transcript)
    return render_template('index.html')

def process_transcript(transcript):
    headers = {
        "authorization": ASSEMBLYAI_API_KEY,
        "content-type": "application/json"
    }

    # Check if API key is set
    if not ASSEMBLYAI_API_KEY:
        raise ValueError("ASSEMBLYAI_API_KEY is not set")

    # Punctuation and Casing
    try:
        response = requests.post(
            "https://api.assemblyai.com/v2/punctuate",
            json={"text": transcript},
            headers=headers
        )
        response.raise_for_status()
        print(f"Punctuation API response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error during punctuation API call: {e}")
        raise

    response_data = response.json()
    punctuated_text = response_data.get('text', '')

    # Inverse Text Normalization (ITN)
    try:
        response = requests.post(
            "https://api.assemblyai.com/v2/itn",
            json={"text": punctuated_text},
            headers=headers
        )
        response.raise_for_status()
        print(f"ITN API response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error during ITN API call: {e}")
        raise

    response_data = response.json()
    itn_text = response_data.get('text', '')

    return itn_text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)