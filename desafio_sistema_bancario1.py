def exibe_tela_inicial():
    print(
        """
    ============= MENU =============

    d - Depositar
    s - Sacar
    e - Extrato
    u - Criar usuário
    c - Criar conta
    q - Sair

    ================================

    Selecione uma opção
    """
    )


def exibe_operacao(valor, saldo, operacao):

    while True:
        clear()
        print(
            f"""
    {operacao.upper()} REALIZADO 
    ===============================
    {operacao} no valor de R$ {valor:.2f}
    Saldo atual: R$ {saldo:.2f}
    ===============================

    Obrigado por usar nosso sistema!!!!
    
    Qualquer tecla para voltar ao menu
    """
        )
        input()
        break


def exibe_extrato(saldo, /, *, extrato):
    while True:
        clear()
        print(
            f"""
                    EXTRATO"""
        )
        print(tabulate(extrato, tablefmt="fancy_grid"))
        print(
            f"""
    Saldo consolidado: {saldo:.2f}

    Obrigado por usar nosso sistema!!!!

    Qualquer tecla para voltar ao menu
    """
        )
        input()
        break


def depositar(saldo, valor, /):

    sucesso = False

    if valor <= 0:
        erro("O valor do depósito deve ser maior que R$ 0,00!")
    else:
        sucesso = True
        saldo += valor

    return sucesso, saldo


def sacar(*, limite_valor_saque, limite_saques, numero_saques, saldo, valor):

    sucesso = False

    if numero_saques >= limite_saques:
        erro("Você atingiu o limite de 3 saques diários.")
    elif valor > limite_valor_saque:
        erro(f"O limite de valor do saque é de R$ {LIMITE_VALOR_SAQUE:.2f}!!!")
    elif saldo < valor:
        erro("Saldo insuficiente!!!")
    elif valor <= 0:
        erro("O valor do saque deve ser maior que R$ 0,00!!!")
    else:
        sucesso = True
        saldo -= valor
        numero_saques += 1

    return sucesso, saldo, numero_saques


def grava_extrato(operacao, valor, saldo, extrato):
    data_hora = datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
    index = len(extrato)
    valor = "R$ {:,.2f}".format(valor)
    saldo = "R$ {:,.2f}".format(saldo)
    extrato.insert(index, [data_hora, operacao, valor, saldo])

    return extrato


def criar_usuario(cadastro_clientes):

    while True:
        clear()
        cpf = input("Informe CPF do usuário: ")
        tamanho = len(str(cpf))
        cpf_existente = cadastro_clientes.get(cpf)

        if not cpf.isdigit() or tamanho != 11:
            erro("CPF inválido!!! Verifique novamente e digite apenas números")
        elif cpf_existente:
            erro("Este usuário já existe!!!")
        else:
            nome = input("Informe nome do usuário: ")
            data_nascimento = input("Informe data de nascimento do usuário: ")
            endereco = input("Informe endereço do usuário: ")

            confirmacao = input(
                "\nDigite ENTER para CONFIRMAR ou outra tecla CANCELAR: \n"
            )

            if confirmacao == "":
                cpf = str(cpf)
                cadastro_clientes = {
                    cpf: {
                        "nome": nome,
                        "data_nascimento": data_nascimento,
                        "endereco": endereco,
                    }
                }
                erro("Usuário criado com sucesso!!!")

            break

    return cadastro_clientes


def criar_conta(cadastro_clientes, numero_conta):

    while True:

        clear()
        cpf = input("Informe CPF para vínculo da conta: ")
        cpf = str(cpf)
        cpf_existente = cadastro_clientes.get(cpf)
        if not cpf_existente:
            erro("Usuário não existe, informe CPF de usuário existente!!!")
        else:
            agencia = AGENCIA
            numero_conta += 1

            cadastro_conta = cadastro_clientes[cpf]
            conta = cadastro_conta.get("conta")
            if conta:
                conta.append(numero_conta)
            else:
                conta = [numero_conta]

            cadastro_conta.update({"agencia": agencia})
            cadastro_conta.update({"conta": conta})
            erro("Conta criada com sucesso!!!")
            break

    return cadastro_clientes, numero_conta


def erro(message):
    clear()
    print(message)
    time.sleep(1)


def clear():
    os.system("cls" if os.name == "nt" else "clear")


from tabulate import tabulate
from datetime import datetime
import time
import os

opcao = ""
saldo = float(0)
numero_saques = 0
extrato = [["Data", "Operação", "Valor", "Saldo"]]
cadastro_clientes = {}
numero_conta = 0
conta = []

LIMITE_VALOR_SAQUE = float(500)
LIMITE_SAQUES = 3
AGENCIA = "0001"

while True:

    clear()  ## CLEAR = "\033c"
    exibe_tela_inicial()
    opcao = input()
    sucesso = False

    if opcao == "d":

        while True:
            clear()
            print("Digite o valor a ser depositado ou q para sair:")
            valor_deposito = input()

            if valor_deposito == "q":
                break

            try:
                valor_deposito = float(valor_deposito)  # Tenta converter para float

                sucesso, saldo = depositar(saldo, valor_deposito)

                if sucesso == True:
                    operacao = "depósito"
                    extrato = grava_extrato(operacao, valor_deposito, saldo, extrato)
                    exibe_operacao(valor_deposito, saldo, operacao)
                    break
            except ValueError:
                erro("Digite um valor númerico!!!")

    elif opcao == "s":

        while True:
            clear()
            print("Digite o valor a ser sacado ou q para sair:")
            valor_saque = input()
            if valor_saque == "q":
                break
            try:
                valor_saque = float(valor_saque)  # Tenta converter para float

                sucesso, saldo, numero_saques = sacar(
                    limite_valor_saque=LIMITE_VALOR_SAQUE,
                    limite_saques=LIMITE_SAQUES,
                    numero_saques=numero_saques,
                    saldo=saldo,
                    valor=valor_saque,
                )
                if sucesso == True:
                    operacao = "saque"
                    extrato = grava_extrato(operacao, valor_saque, saldo, extrato)
                    exibe_operacao(valor_saque, saldo, operacao)
                    break
            except ValueError:
                erro("Digite um valor númerico!!!")

    elif opcao == "u":

        cadastro_clientes = criar_usuario(cadastro_clientes)

    elif opcao == "c":

        cadastro_clientes, numero_conta = criar_conta(cadastro_clientes, numero_conta)

    elif opcao == "e":
        clear()
        exibe_extrato(saldo, extrato=extrato)

    elif opcao == "q":
        clear()
        print("Obrigado e volte sempre!!!\n")
        time.sleep(1)
        clear()
        break
    else:
        clear()
        print(
            """
    ================================
            Opcão inválida
    ================================
        """
        )
        time.sleep(1)
