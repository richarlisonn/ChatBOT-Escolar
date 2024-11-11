import openai
import os
from dotenv import load_dotenv

# CHAVE API
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# R
respostas_prontas = {
    "olá": "Olá! Como posso ajudar você hoje?",
    "como você está?": "Estou ótimo, obrigado por perguntar! E você?",
    "sair": "Até logo! Volte quando quiser.",
    "ajuda": "Claro, estou aqui para ajudar! O que você precisa?",
    "Quando volta as aulas?": "As aulas voltam dia 01/02",
    "Quando é o inicio das organização para as voltas as aulas?":"A organização para a volta as aulas começa dia 30/01",
    "Quando começa as provas unificadas do 1 bimestre":"Começa na semana 7 (17/03 e 18/03)",
}

def enviar_mensagem(mensagem, lista_mensagens=[]):
       # Resposta pronta se a mensagem for uma das chaves
    if mensagem.lower() in respostas_prontas:
        resposta = respostas_prontas[mensagem.lower()]
        interacoes["chatbot"] = resposta
        return resposta

    # Se não for uma resposta pronta, envie para o OpenAI API
    interacoes["user"] = mensagem



    try:
        # Envia a mensagem para a API do OpenAI e obtém a resposta
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",
            messages=lista_mensagens,
        )

        # Adiciona a resposta do modelo à lista de mensagens
        lista_mensagens.append(resposta["choices"][0]["message"])

        # Retorna a resposta para exibição
        return resposta["choices"][0]["message"]

    except Exception as e:
        # Tratamento de exceções, por exemplo, problemas de conexão ou falhas de autenticação
        print(f"Erro ao enviar mensagem: {e}")
        return {"content": "Desculpe, houve um erro ao processar a sua solicitação."}

# Loop principal do chatbot
lista_mensagens = []
while True:
    # Recebe a mensagem do usuário
    texto = input("Escreva aqui sua mensagem:")

    if texto.lower() == "sair":
        break
    else:
        # Envia a mensagem para o chatbot e imprime a resposta
        resposta = enviar_mensagem(texto, lista_mensagens)
        print("Chatbot:", resposta["content"])