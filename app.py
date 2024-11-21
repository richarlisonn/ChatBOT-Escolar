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
    """
    Encontra a resposta mais próxima com base na similaridade da pergunta.
    """
    pergunta = pergunta.lower().strip()
    melhor_match = None
    maior_similaridade = 0

    for chave in respostas_prontas.keys():
        # Calcula a similaridade entre a pergunta e cada chave do FAQ
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
        # Configuração de prompt inicial do sistema
        mensagens = [{"role": "system", "content": """
        Você é um chatbot especializado em responder perguntas sobre a escola E.E Carlos Gomes.
        Responda de forma objetiva e com base nos dados fornecidos no FAQ.
        """}]
        
        # Adiciona a pergunta do usuário ao contexto
        mensagens.append({"role": "user", "content": mensagem})

        # Envia as mensagens para o modelo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=mensagens
        )
        
        # Obtém a resposta do modelo
        resposta = response["choices"][0]["message"]["content"]
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
            return jsonify({"response": resposta_faq})

        # Caso contrário, usa o modelo do OpenAI para gerar uma resposta
        resposta = enviar_mensagem(text, session['historico'])
        return jsonify({"response": resposta})

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
