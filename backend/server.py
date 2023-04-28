from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import PegasusTokenizer, PegasusForConditionalGeneration
import os, re, json, pathlib, pdfplumber, docx2txt

os.environ['PYTHONHTTPSVERIFY'] = '0'

app = Flask(__name__, static_folder='../public')
CORS(app, origins='http://localhost:5173')

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

@app.route('/')
def index():
  return app.send_static_file('index.html')

model_name = "google/pegasus-xsum"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name)

@app.route('/', methods=['POST'])
def summarize():
    request_data = request.get_json()
    input_text = request_data['text']
    max_summary_length = request_data['length']
  
    input_list = split_into_sentences(input_text.replace('\n',''))
    stitch = []

    length_factors = length_parameters(max_summary_length)

    for grouped_sentence, grouped_sentence_length in input_list:
        inputs = tokenizer(grouped_sentence, return_tensors='pt')

        summary_ids = model.generate(inputs['input_ids'], max_length=int(length_factors[1]*grouped_sentence_length), min_length=int(length_factors[0]*grouped_sentence_length), no_repeat_ngram_size=4)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        complete_sentences = re.findall('[A-Z][^\.!?]*[\.!?]', summary)
        complete_summary = " ".join(complete_sentences)
        stitch.append(complete_summary)

    return jsonify({'summary':" ".join(stitch)})

@app.route('/file', methods=['POST'])
def upload():
    file = request.files['file']
    filename = file.filename
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

    input_list = split_into_sentences(extracted_text.replace('\n',''))
    stitch = []

    length_factors = length_parameters(length)

    length_divider = len(input_list) if length=='tweet' else 1

    for grouped_sentence, grouped_sentence_length in input_list:
        inputs = tokenizer(grouped_sentence, return_tensors='pt')

        summary_ids = model.generate(inputs['input_ids'], max_length=int((length_factors[1]*grouped_sentence_length)/length_divider), min_length=int((length_factors[0]*grouped_sentence_length)/length_divider), no_repeat_ngram_size=4)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        complete_sentences = re.findall('[A-Z][^\.!?]*[\.!?]', summary)
        complete_summary = " ".join(complete_sentences)
        stitch.append(complete_summary)

    final_summary = " ".join(stitch)

    response_data = {'summary':final_summary}
    return json.dumps(response_data)

if __name__ == "__main__":
  app.run()