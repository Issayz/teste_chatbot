from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv
import os
from time import sleep

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do app Flask
app = Flask(__name__)
app.secret_key = 'alura'

# Configuração da API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def bot(prompt):
    """
    Envia o prompt do usuário para a API da OpenAI e retorna a resposta.
    Tenta novamente em caso de erro até um limite definido.
    """
    maximo_tentativas = 3
    repeticao = 0

    prompt_do_sistema = """
    Você é um chatbot de atendimento a clientes de um e-commerce.
    Você só deve responder perguntas relacionadas ao e-commerce.
    """

    while repeticao < maximo_tentativas:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt_do_sistema},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            # Retorna o conteúdo gerado pelo modelo
            return response.choices[0].message["content"].strip()
        except Exception as erro:
            repeticao += 1
            if repeticao >= maximo_tentativas:
                return f"Erro no GPT: {erro}"
            print("Erro de comunicação com OpenAI:", erro)
            sleep(1)


@app.route("/chat", methods=["POST"])
def chat():
    """
    Rota para processar mensagens enviadas pelo usuário e retornar a resposta do bot.
    """
    # Obtém a mensagem do JSON enviado pelo frontend
    prompt = request.json.get("msg", "")
    if not prompt:
        return jsonify({"erro": "Mensagem não fornecida"}), 400

    # Gera a resposta com o bot
    resposta = bot(prompt)
    return jsonify({"resposta": resposta})


@app.route("/")
def index():
    """
    Rota principal para servir o HTML estático.
    """
    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run(debug=True)
