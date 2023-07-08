from flask import Flask, request, jsonify
from flask_cors import CORS
from usellm import Message, Options, UseLLM
import os

# load environment variables
API_HOST = os.getenv('API_HOST')
# print(f'valor de API HOST: {API_HOST}')

# initialize a Flask app with CORS enabled
app = Flask(__name__)
CORS(app)

# Initialize the service
# service = UseLLM(service_url=API_HOST)
service = UseLLM(service_url="https://usellm.org/api/llm")


@app.route("/", methods=["GET"])
def root():
  return jsonify('Well done!')

@app.route("/generate", methods=["POST"])
def generate():
  # recogemos el formulario (body)
  r_form = request.form

  translate = r_form.get('translate')
  mensaje = r_form.get('message')

  if (translate.lower() == 'true'):
    idioma = r_form.get('lang')
    pregunta = 'puedes traducirme al idioma ' + idioma + ' lo siguiente: ' + mensaje
  else:
    pregunta = mensaje

  # Prepare the conversation
  messages = [
    # Message(role="system", content="You are a helpful assistant."),
    Message(role="user", content=pregunta),
  ]
  options = Options(messages=messages)

  try:
    # Interact with the service
    response = service.chat(options)
  except Exception as error:
    print('Error: ' + repr(error))

  return jsonify(response.content)

def main():
  # app.run(host="", port=8000)
  from waitress import serve
  serve(app, host="0.0.0.0", port=8080)
  print("Server running on  port 8080")


if __name__ == "__main__":
  main()
