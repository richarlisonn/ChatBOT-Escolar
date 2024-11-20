import openai
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("Chave da OpenAI não encontrada. Configure a variável de ambiente OPENAI_API_KEY.")

def enviar_mensagem(mensagem, lista_mensagens=[]):
    # Adiciona a interação do usuário à lista
    lista_mensagens.append({"role": "user", "content": mensagem})

    try:
        # Envia a mensagem para a API da OpenAI
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=lista_mensagens,
        )

        # Adiciona a resposta do modelo à lista de mensagens
        resposta_modelo = resposta["choices"][0]["message"]
        lista_mensagens.append(resposta_modelo)

        return resposta_modelo

    except openai.error.OpenAIError as e:
        print(f"Erro OpenAI: {e}")
        return {"content": "Desculpe, houve um erro ao processar sua solicitação."}
    except Exception as e:
        print(f"Erro desconhecido: {e}")
        return {"content": "Houve um erro inesperado. Tente novamente mais tarde."}

# Loop principal do chatbot
if __name__ == "__main__":
    lista_mensagens = []
    while True:
        texto = input("Escreva aqui sua mensagem ('sair' para encerrar): ")
        if texto.lower() == "sair":
            print("Chatbot: Até logo! Volte quando quiser.")
            break
        resposta = enviar_mensagem(texto, lista_mensagens)
        print("Chatbot:", resposta["content"])
