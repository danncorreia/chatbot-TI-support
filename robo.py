from chatterbot import ChatBot
from difflib import SequenceMatcher
import json 

CONFIANCA_MINIMA = 0.20
NOME_USUARIO = ""
DADOS_CLIENTE = {
    "ID": 0,
    "NOME_CLIENTE": "",
    "DESCRICAO_CHAMADO": "",
    "STATUS_CHAMADO": "",
    "RESPONSAVEL": "",
    "RESOLUCAO": ""
}


def comparar_mensagens(mensagem_digitada, mensagem_candidata):
    confianca = 0.0

    digitada = mensagem_digitada.text
    candidata = mensagem_candidata.text
    if digitada and candidata:
        confianca = SequenceMatcher(None, 
            digitada,
            candidata)
        confianca = round(confianca.ratio(), 2)

    return confianca

def iniciar():
    robo = ChatBot("Robô de Atendimento do IFBA",
                   read_only=True,
                   statement_comparison_function=comparar_mensagens,     
                   logic_adapters=[
                           "chatterbot.logic.BestMatch"
                   ])

    return robo


def executar_robo(robo):
    global NOME_USUARIO
    while True:
        if(NOME_USUARIO == ""):
            NOME_USUARIO = input("Qual o seu nome? \n").upper()
            print("Suporte:", "Oi " + NOME_USUARIO + ", em que posso te ajudar?")
        else:
            mensagem = input(NOME_USUARIO + ": ")
            resposta = robo.get_response(mensagem.lower())
            print(f"o valor da confiança é: {resposta.confidence}")
             
            if resposta.confidence >= CONFIANCA_MINIMA: 
                # print(resposta.text)
                seleciona_action(mensagem, resposta.text)
            else:
                print("Infelizmente, ainda não sei responder isso")
                print("Pergunte outra coisa")

def seleciona_action(message, resposta):
    global DADOS_CLIENTE

    if resposta == "Para quem você quer abrir um chamado?":
        abertura_chamado(input(resposta+": ").upper())
    elif resposta == "Qual o número do chamado que você quer consultar?":
        consultar_chamado(input(resposta +": "))
    elif resposta == "Qual o nome do cliente que você quer consultar os chamados?":
        listar_chamado_cliente(input(resposta+": ").upper())
    elif resposta == "Qual o nome do responsável que você quer consultar os chamados?":
        listar_chamados_responsavel_abertos(input(resposta+": ").upper())
    elif resposta == "Os chamados em aberto são":
        listar_chamados_abertos()
    elif resposta == "Qual o chamado você quer pausar?":
        pausar_chamado(input(resposta+": "))
    elif resposta == "Qual o chamado você quer encerrar?":
        encerrar_chamado(input(resposta+": "))
    else:
        print("Suporte:", resposta)

def abertura_chamado(nome):
    global DADOS_CLIENTE
    
    DADOS_CLIENTE["ID"] = get_new_id()
    DADOS_CLIENTE["NOME_CLIENTE"] = nome
    DADOS_CLIENTE["RESPONSAVEL"] = NOME_USUARIO
    DADOS_CLIENTE["STATUS_CHAMADO"] = "Aberto"
    DADOS_CLIENTE["DESCRICAO_CHAMADO"] = input("Qual a descrição do chamado?: ")
        
    chamados = read_db()
    chamados.append(DADOS_CLIENTE)
    write_db(chamados)

    print("SUPORTE:", "O chamado foi aberto com sucesso! \n")
    print(print_chamado(DADOS_CLIENTE))

    DADOS_CLIENTE = {
        "ID": 0,
        "NOME_CLIENTE": "",
        "DESCRICAO_CHAMADO": "",
        "STATUS_CHAMADO": "",
        "RESPONSAVEL": "",
        "RESOLUCAO": ""
    }

def consultar_chamado(id):
    chamados = read_db()
    for chamado in chamados:
        if chamado["ID"] == id:
            print_chamado(chamado)

def listar_chamado_cliente(nome):
    print(nome)
    chamados = read_db()
    for chamado in chamados:
        if chamado["NOME_CLIENTE"] == nome:
            print_chamado(chamado)

def listar_chamados_responsavel_abertos(nome):
    chamados = read_db()
    for chamado in chamados:
        if chamado["RESPONSAVEL"] == nome:
            print_chamado(chamado)

def listar_chamados_abertos():
    chamados = read_db()
    for chamado in chamados:
        if chamado["STATUS_CHAMADO"] == "Aberto":
            print_chamado(chamado)

def pausar_chamado(id):
    chamados = read_db()
    for chamado in chamados:
        if chamado["ID"] == id:
            chamado["RESOLUCAO"] = input("Qual a resolução do chamado?: ")
            chamado["STATUS_CHAMADO"] = "Pausado"
            write_db(chamados)
            return
    print("SUPORTE:", "Chamado não encontrado! \n")

def encerrar_chamado(id):
    chamados = read_db()
    for chamado in chamados:
        if chamado["ID"] == id:
            chamado["STATUS_CHAMADO"] = "Encerrado"
            write_db(chamados)
            return
    print("SUPORTE:", "Chamado não encontrado! \n")

def read_db():
    with open("db_chamados.json", "r") as arquivo:
        chamados = json.load(arquivo)
        arquivo.close()

    return chamados["CHAMADOS"]

def write_db(chamados):
    with open("db_chamados.json", "w") as arquivo:
        json.dump({"CHAMADOS":chamados}, arquivo)
        arquivo.close()

def get_new_id():
    chamados = read_db()
    if len(chamados) == 0:
        return 1
    else:
        return chamados[-1]["ID"] + 1

def print_chamado(chamado):
    print("Cliente: "+chamado["NOME_CLIENTE"]
          +"\nNúmero do chamado: "+str(chamado["ID"])
          +"\nDescrição: "+chamado["DESCRICAO_CHAMADO"]
          +"\nStatus: "+chamado["STATUS_CHAMADO"]
          +"\nResponsável: "+chamado["RESPONSAVEL"]
    )

    print("\nResolução: "+chamado["RESOLUCAO"]) if chamado["STATUS_CHAMADO"] != "Aberto" else "" + "\n"
    print("\n")

if __name__ == "__main__":
    robo = iniciar()

    executar_robo(robo)
