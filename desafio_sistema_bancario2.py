def main():
    cpf,senha,agencia,conta=login()
    if senha == None or agencia == None:
        return

    saldo,LIMITE_VALOR_SAQUE,numero_saques,LIMITE_QUANTIDADE_SAQUES=inicializacao(cpf,agencia,conta)
    
    while True:
        
        opcao=menu()

        if opcao == '1': # deposito
            saldo=deposito(float(input('Digite o valor desejado para o deposito:')),saldo,cpf,agencia,conta)

        elif opcao == '2': # saque
            saldo,numero_saques=saque(valor=float(input('Digite o valor desejado para o saque:')),
            saldo=saldo,LIMITE_VALOR_SAQUE=LIMITE_VALOR_SAQUE,numero_saques=numero_saques,
            LIMITE_QUANTIDADE_SAQUES=LIMITE_QUANTIDADE_SAQUES,cpf=cpf,agencia=agencia,conta=conta)

        elif opcao == '3': # extrato
            _extrato(cpf,agencia,conta)
            
        elif opcao == '4': # cadastro de novas contas
            nova_conta(cpf,conta)
        
        elif opcao == '5': # sair
            break
        
        else:
            print('Digite uma opçao válida')

def login():
    cpf=input('Favor digitar o CPF (somente numeros):')
    with open('Clientes_Cadastrados2.txt','r') as file:
            for line in file: #obtençao do nome do usuario
                if cpf in line:
                    usuario=line.split(',')
                    usuario_nome=usuario[1]
                    senha=input('Favor digitar sua senha:')
                    if senha == usuario[2]: #confirmaçao da senha
                        if usuario[5]=='fim\n': # exibicao do nome e contas atreladas
                            print(f'Bem vindo(a) {usuario[1]}: Agencia: {usuario[3]}, Conta: {usuario[4]}')
                        else:
                            print(f'Bem vindo(a) {usuario[1]}: Agencia: {usuario[3]}, Contas: {usuario[4]} e {usuario[5]}') 
                        conta=input('Entre com o numero da sua conta:')
                        if conta == usuario[4] or conta == usuario[5]:
                            agencia=usuario[3]
                            return cpf,senha,agencia,conta
                        else:
                            print('=> Conta inválida.')
                            return cpf,senha,None,None
                    else: 
                        print('=> Senha inválida.')
                        return cpf,None,None,None
            else:
                cpf,senha,agencia,conta=criar_usuario(cpf)
                return cpf,senha,agencia,conta

def criar_usuario(cpf):
    nome=input('Entre com seu nome completo:')
    senha=input('Crie uma senha de 4 numeros:')
    agencia,conta=criar_conta_corrente(cpf)
    impressao=(f'{cpf},{nome},{senha},{agencia},{conta},fim\n')
    with open('Clientes_Cadastrados2.txt','a') as file:
        file.write(impressao)  
    return cpf,senha,agencia,conta

def criar_conta_corrente(cpf):
    agencia='0001'
    with open('Contas.txt','r') as file:
        for line in file:
            conta=line
    file = open(f'{cpf}_{agencia}_{conta}.txt','w')
    data,dia=data_time()
    file.write(f'Saldo    : {data},  Valor: R$0.00\n')
    conta=int(conta)
    conta+=1
    with open('Contas.txt','w') as file:
        file.write(f'{conta}')
    return agencia,conta-1

def nova_conta(cpf,conta):
    with open('Clientes_Cadastrados2.txt','r') as file:
        for line in file: #obtençao do nome do usuario
            if cpf in line:
                usuario=line.split(',')
        if len(usuario) == 7:
            print('=> Cada usuário pode ter no máximo duas contas distintas.')
            return
    # leitura do arquivo dos clientes cadastrados e carregamento dos dados numa variavel temporaria (arquivo)
    with open('Clientes_Cadastrados2.txt','r') as file:
        arquivo=file.read()
    # criaçao de nova conta sequencial e inclusao nos dados do cliente selecionado
    agencia,nova_conta=criar_conta_corrente(cpf)
    novo_arquivo=arquivo.replace(f'{conta},fim',f'{conta},{nova_conta},fim')
    # inclusao dos dados alterados no arquivo dos clientes cadastrados
    with open('Clientes_Cadastrados2.txt','w') as file:
        file.write(novo_arquivo)
    print (f'=> Conta de numero {nova_conta} foi cadastrada com sucesso.')

def inicializacao(cpf,agencia,conta):
    saldo=ler_saldo(cpf,agencia,conta)
    LIMITE_VALOR_SAQUE = 500
    numero_saques = 0
    LIMITE_QUANTIDADE_SAQUES = 3
    # LIMITE_CONTAS=2
    return saldo,LIMITE_VALOR_SAQUE,numero_saques,LIMITE_QUANTIDADE_SAQUES

def data_time():
    from datetime import datetime
    now = datetime.now()
    data = now.strftime("%d/%m/%Y %H:%M:%S")
    dia = now.strftime("%d/%m/%Y")
    return data,dia

def ler_saldo(cpf,agencia,conta):
    with open(f'{cpf}_{agencia}_{conta}.txt','r') as file:
            for line in file:
                if 'Saldo' in line:
                    dividir_linha=line.split(' ')
                    saldo=dividir_linha[-1]
                    saldo_formatado=saldo
                    saldo=float(saldo.replace('R$',''))
            print('Saldo atual:',saldo_formatado)
            return saldo

def _extrato(cpf,agencia,conta):
    with open(f'{cpf}_{agencia}_{conta}.txt','r') as file:
        print('\n####################################### EXTRATO #######################################\n')
        for line in file:
            print(line,end='')
        print('\n#######################################################################################\n')

def menu():
    print( """

    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Cadastro de nova conta
    [5] Sair

    """)
    opcao = input('Digite uma das opcões acima:')
    return opcao

def deposito(*args):
    valor,saldo,cpf,agencia,conta = args
    if valor > 0:
        saldo += valor
        data,dia=data_time()
        impressao= (f'Deposito - Data e hora: {data},  Valor: +R${valor:.2f},  Saldo: R${saldo:.2f}\n')
        with open(f'{cpf}_{agencia}_{conta}.txt','a') as file:
            file.write(impressao)  
    else:
        print('=> Valor invalido')
    return saldo

def saque(**kwargs):
    valor,saldo,LIMITE_VALOR_SAQUE,numero_saques,LIMITE_QUANTIDADE_SAQUES,cpf,agencia,conta = kwargs.values()
    ## contagem do numero de saques
    numero_saques=0
    data,dia=data_time()
    with open(f'{cpf}_{agencia}_{conta}.txt','r') as file:
        for line in file:
            if f'Saque    - Data e hora: {dia}' in line:
                numero_saques +=1
    ##
    if numero_saques >= LIMITE_QUANTIDADE_SAQUES:
        print('=> Limite de saques (3 saques por dia) excedido.')
    elif valor > LIMITE_VALOR_SAQUE:
        print('=> Limite de valor (R$500,00) excedido.')
    elif valor > saldo:
        print('=> Saldo insuficiente.')
    elif valor > 0:            
        saldo -= valor
        data,dia=data_time()
        impressao= (f'Saque    - Data e hora: {data},  Valor: -R${valor:.2f},  Saldo: R${saldo:.2f}\n')
        with open(f'{cpf}_{agencia}_{conta}.txt','a') as file:
            file.write(impressao)  
    else:
        print('=> Valor inválido, tente novamente.')
    return saldo, numero_saques

main()