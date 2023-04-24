from flask import Flask, request, jsonify
from transformers import PegasusTokenizer, PegasusForConditionalGeneration
import os
from flask_cors import CORS

os.environ['PYTHONHTTPSVERIFY'] = '0'

app = Flask(__name__, static_folder='../public')
CORS(app, origins='http://localhost:5173')

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
  max_summary_length = int(request_data['length'])
    
  inputs = tokenizer(input_text, return_tensors='pt')

  # Generate summary
  summary_ids = model.generate(inputs['input_ids'], max_length=max_summary_length, min_length=56, early_stopping=True)
  summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

  # Return the summary as a JSON response
  return jsonify({'summary': summary})

if __name__ == "__main__":
  app.run()


# from transformers import PegasusTokenizer, PegasusForConditionalGeneration, pipeline # change model if required: ModelClass...

# model_name = "google/pegasus-xsum"
# pegasus_tokenizer = PegasusTokenizer.from_pretrained(model_name)
# pegasus_model = PegasusForConditionalGeneration.from_pretrained(model_name)

# input_text = '''Deep learning (also known as deep structured learning) is part of a broader family of machine learning methods based on artificial neural networks with representation learning. Learning can be supervised, semi-supervised or unsupervised. Deep-learning architectures such as deep neural networks, deep belief networks, deep reinforcement learning, recurrent neural networks and convolutional neural networks have been applied to fields including computer vision, speech recognition, natural language processing, machine translation, bioinformatics, drug design, medical image analysis, material inspection and board game programs, where they have produced results comparable to and in some cases surpassing human expert performance. Artificial neural networks (ANNs) were inspired by information processing and distributed communication nodes in biological systems. ANNs have various differences from biological brains. Specifically, neural networks tend to be static and symbolic, while the biological brain of most living organisms is dynamic (plastic) and analogue. The adjective "deep" in deep learning refers  to the use of multiple layers in the network. Early work showed that a linear perceptron cannot be a universal classifier, but that a network with a nonpolynomial activation function with one hidden layer of unbounded width can. Deep learning is a modern variation which is concerned with an unbounded number of layers of bounded size, which permits practical application and optimized implementation, while retaining theoretical universality under mild conditions. In deep learning the layers are also permitted to be heterogeneous and to deviate widely from biologically informed connectionist models, for the sake of efficiency, trainability and understandability, whence the structured part.'''

# tokens = pegasus_tokenizer(input_text, return_tensors="pt") # last argument returns TensorType - TensorFlow variable type, pt for PyTorch
# encoded_summarized_text = pegasus_model.generate(**tokens) # ** to unpack the dictionary
# decoded_summarized_text = pegasus_tokenizer.decode(encoded_summarized_text[0])

# print("One-line summary:\n", decoded_summarized_text, end="\n\n")

# summarizer = pipeline(task="summarization",
#                       model=pegasus_model, tokenizer=pegasus_tokenizer)
# summary = summarizer(input_text, min_length=30, max_length=60)

# print("Customized summary:\n", summary[0]['summary_text'], end="\n")