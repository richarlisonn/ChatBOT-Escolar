from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv
import os

# Configure sua chave da OpenAI (Certifique-se de configurar a chave corretamente)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Rota principal
@app.route("/", methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        text = request.form.get('prompt')  # Obtém a mensagem do usuário
        
        # Chama a função que envia a mensagem para a API
        resposta = enviar_mensagem(text)

        # Retorna a resposta para o frontend
        return jsonify({"response": resposta['content']})

    return render_template("index.html")

def enviar_mensagem(mensagem):
    try:
        # Envia a mensagem para o modelo GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": mensagem}]
        )
        
        # Retorna a resposta do modelo
        return response["choices"][0]["message"]

    except Exception as e:
        # Em caso de erro, exibe uma mensagem padrão
        return {"content": "Desculpe, houve um erro ao processar a sua solicitação."}

if __name__ == "__main__":
    app.run(debug=True)

