from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import PegasusTokenizer, PegasusForConditionalGeneration
from time import sleep
import os, re, json, pathlib, pdfplumber, docx2txt, requests, cloudinary, cloudinary.uploader

os.environ['PYTHONHTTPSVERIFY'] = '0'

app = Flask(__name__, static_folder='../public')
CORS(app, origins='http://localhost:5173')

model_name = "google/pegasus-xsum"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name)

cloudinary.config(
    cloud_name = "dy8ofvrgh",
    api_key = "885785725818619",
    api_secret = "Y28WJo5fpKR6M6GIw3f73dQLiNY"
)

API_key = "52311c92105d4cb2a7ba3baacd495ed7"

headers = headers = {
    'authorization': API_key, 
    'content-type': 'application/json',
}

transcription_endpoint = "https://api.assemblyai.com/v2/transcript"

def length_parameters(summary_length_choice):
    summary_length_factors = {
        "short": (0.15, 0.2),
        "medium": (0.3, 0.4),
        "long": (0.6, 0.7),
        "tweet": (0.27, 0.27)
    }
    
    return summary_length_factors[summary_length_choice]

def split_into_sentences(text):
    sentences = re.findall('[A-Z][^\.!?]*[\.!?]', text)
    sentence_tokens = []

    for sentence in sentences:
        tokenized_sentence = tokenizer(sentence)
        sentence_tokens.append(len(tokenized_sentence['input_ids']))

    max_token_length = 512
    current_token_length = sentence_tokens[0]
    current_sentence = sentences[0]
    result = []
    for sentence_token, sentence in zip(sentence_tokens[1:], sentences[1:]):
        if current_token_length + sentence_token < max_token_length:
            current_token_length += sentence_token
            current_sentence += ' ' + sentence
        else:
            result.append((current_sentence, len(tokenizer(current_sentence)['input_ids'])))
            current_token_length = sentence_token
            current_sentence = sentence
    
    result.append((current_sentence, len(tokenizer(current_sentence)['input_ids'])))

    return result

def summarize(input_text, summary_length):
    input_list = split_into_sentences(input_text.replace('\n',''))
    stitch = []

    length_factors = length_parameters(summary_length)
    length_divider = len(input_list) if summary_length=='tweet' else 1

    for grouped_sentence, grouped_sentence_length in input_list:
        inputs = tokenizer(grouped_sentence, return_tensors='pt')

        summary_ids = model.generate(inputs['input_ids'], max_length=int((length_factors[1]*grouped_sentence_length)/length_divider), min_length=int((length_factors[0]*grouped_sentence_length)/length_divider), no_repeat_ngram_size=4)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        complete_sentences = re.findall('[A-Z][^\.!?]*[\.!?]', summary)
        complete_summary = " ".join(complete_sentences)
        stitch.append(complete_summary)

    return " ".join(stitch)

def audio_upload(afile):
    upload_response = cloudinary.uploader.upload(afile, resource_type="video")

    return upload_response["url"]

def set_json(summary_type, url):
    json_type = {
        "conversational": {"audio_url": url, "auto_chapters": True, "punctuate": True, "format_text": True, "summary_model": "conversational", "summary_type": "paragraph", "speaker_labels": False, "dual_channel": True},

        "informative": {"audio_url": url, "auto_chapters": True, "punctuate": True, "format_text": True, "summary_model": "informative", "summary_type": "paragraph"}
    }

    return json_type[summary_type]

def transcribe(upload_url, type): 

    json = set_json(type, upload_url)
    
    response = requests.post(transcription_endpoint, json=json, headers=headers)
    transcription_id = response.json()['id']

    return transcription_id

def get_result(transcription_id): 

    current_status = "queued"

    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcription_id}"

    while current_status not in ("completed", "error"):
        
        response = requests.get(endpoint, headers=headers)
        current_status = response.json()['status']
        
        if current_status in ("completed", "error"):
            return response.json()
        else:
            sleep(10)

@app.route('/')
def index():
  return app.send_static_file('index.html')

@app.route('/', methods=['POST'])
def text():
    request_data = request.get_json()
    input_text = request_data['text']
    max_summary_length = request_data['length']
  
    final_summary = summarize(input_text, max_summary_length)
    
    return jsonify({'summary':final_summary})

@app.route('/file', methods=['POST'])
def upload():
    file = request.files['file']
    filename = file.filename
    print(filename)
    file_ext = pathlib.Path(filename).suffix
    extracted_text = ''

    match file_ext:
        case '.pdf':
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    extracted_text += page.extract_text()
        case '.docx' | '.doc':
            extracted_text = docx2txt.process(file)
        case '.txt':
            extracted_text = file.read().decode('utf-8')

    length = request.form['length']

    final_summary = summarize(extracted_text, length)
    
    response_data = {'summary':final_summary}
    return json.dumps(response_data)

@app.route('/audio', methods=['POST'])
def audio():
    audio_file = request.files['file']
    summary_type = request.form['type']

    upload_url = audio_upload(audio_file)
    transcription_id = transcribe(upload_url, summary_type)
    response = get_result(transcription_id)

    summary = []

    for chapter in response['chapters']:
        summary.append(chapter['summary'])

    final_summary = " ".join(summary)

    final_response = {'text': response['text'],'summary': final_summary}

    return json.dumps(final_response)

if __name__ == "__main__":
  app.run(debug=True)