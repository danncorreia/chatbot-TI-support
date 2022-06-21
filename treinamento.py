from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import json

CONVERSAS = [
    "conversas/saudacoes.json",
    "conversas/informacoes_basicas.json",
    "conversas/chamado.json"
]

def iniciar():
    robo = ChatBot("Robô de Atendimento do Suporte Técnico")
    treinador = ListTrainer(robo)

    return treinador

def carregar_conversas():
    conversas = []

    for arquivo_conversas in CONVERSAS:
        with open(arquivo_conversas, "r") as arquivo:
            conversas_para_treinamento = json.load(arquivo)
            conversas.append(conversas_para_treinamento["conversas"])

            arquivo.close()

    return conversas

def treinar(treinador, conversas):
    for conversa in conversas:
        for mensagens_resposta in conversa:
            mensagens = mensagens_resposta["mensagens"]
            resposta = mensagens_resposta["resposta"]

            print(f"treinando o robô. Mensagens: {mensagens}. Resposta: {resposta}")
            for mensagem in mensagens:
                treinador.train([mensagem, resposta])


if __name__ == "__main__":
    treinador = iniciar()

    conversas = carregar_conversas()
    if conversas:
        treinar(treinador, conversas)
