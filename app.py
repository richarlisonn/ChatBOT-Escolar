import openai
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
import os
import json
from difflib import SequenceMatcher

# Carregar variáveis de ambiente
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Configurar chave secreta para o Flask usar sessões
app.secret_key = 'sua_chave_secreta_aqui'  # Troque por uma chave secreta real

# Função para carregar o FAQ de um arquivo JSON
def carregar_faq(arquivo="faq.json"):
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            faq = json.load(f)
            print("FAQ carregado com sucesso:", faq)  # Depuração
            return faq
    except Exception as e:
        print(f"Erro ao carregar o FAQ: {e}")
        return {}

# Carregar FAQ
respostas_prontas = carregar_faq()

# Função para encontrar a resposta mais próxima no FAQ
def get_closest_faq_answer(pergunta, threshold=0.6):
    pergunta = pergunta.lower().strip()
    melhor_match = None
    maior_similaridade = 0

    for chave in respostas_prontas.keys():
        similaridade = SequenceMatcher(None, pergunta, chave.lower()).ratio()
        if similaridade > maior_similaridade and similaridade >= threshold:
            melhor_match = chave
            maior_similaridade = similaridade

    if melhor_match:
        return respostas_prontas[melhor_match]
    return None

# Função para enviar a mensagem para a API da OpenAI
def enviar_mensagem(mensagem, lista_mensagens):
    try:
        # Adiciona a mensagem do usuário ao histórico
        lista_mensagens.append({"role": "user", "content": mensagem})
        
        # Envia a sequência de mensagens para o modelo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # ou o modelo que você está usando
            messages=lista_mensagens
        )
        
        # Obtenha a resposta do modelo
        resposta = response["choices"][0]["message"]["content"]

        # Adiciona a resposta do modelo ao histórico
        lista_mensagens.append({"role": "assistant", "content": resposta})
        
        return resposta
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
        return "Desculpe, houve um erro inesperado. Tente novamente mais tarde."

# Rota principal
@app.route("/", methods=['GET', 'POST'])
def homepage():
    # Inicializa o histórico de mensagens
    if 'historico' not in session:
        session['historico'] = []

    if request.method == 'POST':
        text = request.form.get('prompt', '').strip()
        if not text:
            return jsonify({"response": "Por favor, digite algo para que eu possa ajudar."})

        # Verifica no FAQ primeiro
        resposta_faq = get_closest_faq_answer(text)
        if resposta_faq:
            # Caso encontre no FAQ, retorna essa resposta
            return jsonify({"response": resposta_faq})

        # Caso contrário, usa o modelo do OpenAI para gerar uma resposta com base no histórico
        resposta = enviar_mensagem(text, session['historico'])
        
        # Retorna a resposta do modelo
        return jsonify({"response": resposta})

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
