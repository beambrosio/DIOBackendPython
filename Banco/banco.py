saldo = 0
LIMITE = 500
extrato = ""
numero_saque = 0
MAX_SAQUE = 3
list_user = []
list_cc = []

def func_saque(*,saldo, qtd_saque, extrato, LIMITE, numero_saque):
    if numero_saque <= MAX_SAQUE:
        if qtd_saque <= LIMITE:
            if qtd_saque <= saldo:
                saldo = (saldo - qtd_saque)
                numero_saque +=1
                extrato += (f"Saque: R${qtd_saque:.2f}\n")
            else:
                print("Saque maior que o Saldo")
        else:
            print("Max de R$500,00 por saque")
    else:
        print("Limite de Saque diário")
    return saldo, extrato

def func_deposito(saldo, ver_saldo, extrato, /):
    if ver_saldo >= 0: 
        saldo += ver_saldo
        extrato += (f'Depósito: R$ {ver_saldo}\n')
    else:
        print(f"Valor Errado. Valor: R${saldo}")
    return saldo, extrato

def func_extrato(saldo,/,*, extrato):
    return print(f"\nExtrato\n{extrato}\n Saldo atual: R${saldo:.2f}")

def criar_cc(cpf):
    AGENCIA = '0001'
    inc_conta = (len(list_cc) + 1)
    new_cc = dict(user_cpf = cpf, conta = inc_conta, agencia = AGENCIA)
    user_exists = filtrar_cpf(cpf, list_user)
    if user_exists:
        new_cc.update(user_exists)
        list_cc.append(new_cc)
    else:
        print(f'cpf nao esta cadastrado, criar o usuario')

    print(f"""
          ================ CONTA CORRENTE ==============  
          \tNome: {new_cc['nome_user']},
          \tAgencia: {new_cc['agencia']},
          \tConta Corrente: {new_cc['conta']}\n
        """)
    
    return list_cc

def criar_client(nome, dt_nasc, cpf, endereco):
    new_user = dict(nome_user=nome, dt_nasc_user=dt_nasc, cpf_user=cpf, endereco_user=endereco)
    if len(list_user) == 0:
        list_user.append(new_user)
    else:
        user_exists = filtrar_cpf(cpf, list_user)
        if user_exists:
            print(f"CPF {user_exists['cpf_user']} ja registrado")
        else:
            list_user.append(new_user)

        print(f"""
            ========= USUARIO CRIADO COM SUCESSO =========
            \tNome: {new_user['nome_user']},
            \tData de Nascimento: {new_user['dt_nasc_user']},
            \tCPF: {new_user['cpf_user']},
            \tEndereço: {new_user['endereco_user']}
            """)  
        
    return list_user

def listar_cc(list_cc):
    for each in list_cc:
        print(f"""
            \tNome: {each['nome_user']},
            \tAgencia: {each['agencia']},
            \tConta Corrente: {each['conta']}
            \t====================================
        """)

def listar_client(list_user):
    for each in list_user:
        print(f"""
            \tNome: {each['nome_user']},
            \tData de Nascimento: {each['dt_nasc_user']},
            \tCPF: {each['cpf_user']},
            \tEndereço: {each['endereco_user']}
            \t====================================
        """)

def filtrar_cpf(cpf, list_user):
    for each in list_user:
        if each["cpf_user"] == cpf:
            found_user = each
        else:
            found_user = []
    return found_user

menu = """
 --- MENU --- 

1 - Sacar
2 - Deposito
3 - Extrato
4 - Criar Conta Corrente 
5 - Criar Cliente
6 - Todas CC
7 - Todos Usuarios
8 - Sair

Digite a opção escolhida: """


print(
    '''\n --- Sistema de Banco --- \n'''
    )

while True:

    opcao = input(menu)

    if opcao == "1":
        print("\n--- Sacar ---")
        qtd_saque = float(input("Valor a sacar: R$\n"))
        saldo, extrato = func_saque(saldo, qtd_saque, extrato, LIMITE, numero_saque)
        print(f"Saldo: {saldo}")
        
    elif opcao == "2":
        print("\n--- Depósito ---")
        ver_saldo = float(input("Valor a depositar: R$"))
        saldo, extrato = func_deposito(saldo, ver_saldo, extrato)
        print(f"Saldo atualizado: R${saldo:.2f}\n")

    elif opcao == "3":
        print("\n--- Extrato ---")
        func_extrato(saldo, extrato)

    elif opcao == "4":
        print("\n--- Criar Conta Corrente ---")   
        user_cc = input("Digite o CPF do usuário: ") 
        cc = criar_cc(user_cc)
                
    elif opcao == "5":
        print("\n--- Criar Cliente ---") 
        nome = str(input("Nome: "))
        dt_nasc = input("Data de Nascimento: ")
        cpf = input("CPF: ")
        
        logradouro = str(input("Logradouro: "))
        nro = input("Número: ")
        bairro = str(input("Bairro: "))
        cidade = str(input("Cidade: "))
        estado =  str(input("Estado: "))
        
        cidade_estado = cidade, estado
        cidade_estado = "/".join(cidade_estado)
        endereco = logradouro, nro, bairro, cidade_estado
        endereco = " - ".join(endereco)

        cliente = criar_client(nome, dt_nasc, cpf, endereco)

    elif opcao == "6":
        print("Listar Todas as Contas Correntes")
        listar_cc(cc)
    elif opcao == "7":    
        print("Listar todos os Usuários")
        listar_client(cliente)
    elif opcao == "8":
        print("Sair do Sistema")
        break;