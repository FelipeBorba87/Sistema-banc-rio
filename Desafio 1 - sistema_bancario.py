def exibe_tela_inicial():
    print(
        """
    ============= MENU =============

    d - Depositar
    s - Sacar
    e - extrato
    q - Sair

    ================================

    Selecione uma opção
    """
    )


def opcao_invalida():

    print(CLEAR)
    print(
        """
        ====================================
                Opcão inválida
        ====================================
        """
    )
    time.sleep(1)


def exibe_operacao(valor, saldo, operacao):

    while True:
        print(CLEAR)
        print(
            f"""
    ============= {operacao.upper()} =============
    {operacao} no valor de R$ {valor:.2f}
    Saldo atual: R$ {saldo:.2f}
    ===================================

    Obrigado por usar nosso sistema!!!!
    
    Enter - voltar ao menu
    """
        )

        acao = input()
        if acao != "":
            opcao_invalida()
        else:
            break


def exibe_extrato(extrato):
    while True:
        print(CLEAR)
        print(
            f"""
                     EXTRATO                 """
        )
        print(tabulate(extrato, tablefmt="fancy_grid"))
        print(
            """

        Obrigado por usar nosso sistema!!!!

        Enter - voltar ao menu
        """
        )
        acao = input()
        if acao != "":
            opcao_invalida()
        else:
            break


def depositar(saldo, valor):

    sucesso = False
    if type(valor) != str:

        if valor <= 0:
            erro("O valor do depósito deve ser maior que R$ 0,00!")
        else:
            sucesso = True
            saldo += valor
    else:
        erro("Digite um valor númerico maior que R$ 0,00!")

    return sucesso, saldo


def sacar(limite_valor_saque, limite_saques, numero_saques, saldo, valor):

    sucesso = False
    if numero_saques >= limite_saques:
        erro("Você atingiu o limite de 3 saques diários.")
    else:
        if type(valor) != str:

            if valor > limite_valor_saque:
                erro(f"O limite de valor do saque é de R$ {LIMITE_VALOR_SAQUE:.2f}")
            else:
                if valor <= 0:
                    erro("O valor do saque deve ser maior que R$ 0,00")
                else:
                    if saldo < valor:
                        erro("Saldo insuficiente")
                    else:
                        sucesso = True
                        saldo -= valor
                        numero_saques += 1
        else:
            erro("Digite um valor númerico")

    return sucesso, saldo, numero_saques


def grava_extrato(operacao, valor, saldo, extrato):
    data_hora = datetime.now()
    data_hora = data_hora.strftime("%m/%d/%Y - %H:%M:%S")
    index = len(extrato)
    valor = "R$ {:,.2f}".format(valor)
    saldo = "R$ {:,.2f}".format(saldo)
    extrato.insert(index, [data_hora, operacao, valor, saldo])

    return extrato


def erro(message):
    print(CLEAR)
    print(message)
    time.sleep(1)


from tabulate import tabulate

from datetime import datetime
import time

opcao = ""
saldo = float(0)
numero_saques = 0
extrato = [["Data", "Operação", "Valor", "Saldo"]]

LIMITE_VALOR_SAQUE = float(500)
CLEAR = "\033c"
LIMITE_SAQUES = 3


while True:

    print(CLEAR)
    exibe_tela_inicial()
    opcao = input()
    sucesso = False

    if opcao == "d":

        while True:
            print(CLEAR)
            print("Digite o valor a ser depositado ou q para sair:")
            valor_deposito = input()

            if valor_deposito == "q":
                break
            else:
                try:
                    valor_deposito = float(valor_deposito)  # Tenta converter para float
                    sucesso, saldo = depositar(saldo, valor_deposito)
                except ValueError:
                    erro("Digite um número!!!")

            if sucesso == True:
                operacao = "depósito"
                exibe_operacao(valor_deposito, saldo, operacao)
                extrato = grava_extrato(operacao, valor_deposito, saldo, extrato)
                break

    elif opcao == "s":

        while True:
            print(CLEAR)
            print("Digite o valor a ser sacado ou q para sair:")
            valor_saque = input()

            if valor_saque == "q":
                break
            else:
                try:
                    valor_saque = float(valor_saque)  # Tenta converter para float
                    sucesso, saldo, numero_saques = sacar(
                        LIMITE_VALOR_SAQUE,
                        LIMITE_SAQUES,
                        numero_saques,
                        saldo,
                        valor_saque,
                    )
                except ValueError:
                    erro("Digite um número!!!")

            if sucesso == True:
                operacao = "saque"
                exibe_operacao(valor_saque, saldo, operacao)
                extrato = grava_extrato(operacao, valor_saque, saldo, extrato)
                break

    elif opcao == "e":
        print(CLEAR)
        exibe_extrato(extrato)

    elif opcao == "q":
        print(CLEAR)
        print("Obrigado e volte sempre!!!")
        time(1)
        break
    else:
        opcao_invalida()
