
menu = """\n
 --- MENU --- 
1 - Depositar
2 - Sacar
3 - Extrato
4 - Sair\n

Digite a opção escolhida: """
saldo = 0
limite = 500
extrato = ""
numero_saque = 0
max_saque = 3


print(
    '''\n --- Sistema de Banco --- \n'''
    )

while True:

    opcao = input(menu)

    if opcao == "1":
        print("\n--- Depósito ---")
        ver_saldo = float(input("Valor a depositar: R$"))
        if ver_saldo >= 0: 
            saldo = ver_saldo + saldo
            extrato += (f'Depósito: R$ {ver_saldo}\n')
            print(f"Saldo atualizado: R${saldo:.2f}\n")
        else:
            print(f"Valor Errado. Valor: R${saldo}")
    elif opcao == "2":
        print("\n--- Sacar ---")
        if numero_saque <= max_saque:
            qtd_saque = float(input("Valor a sacar: R$\n"))
            if qtd_saque <= limite:
                if qtd_saque <= saldo:
                    saldo = (saldo - qtd_saque)
                    numero_saque +=1
                    extrato += (f"Saque: R${qtd_saque:.2f} | Qtd de Saques(max 3 diário): {numero_saque}\n")
                else:
                    print("Saque maior que o Saldo")
            else:
                print("Max de R$500,00 por saque")
        else:
            print("Limite de Saque diário")
        print(f"Voce fez {numero_saque} saque. Saldo Atualizado: R${saldo:.2f}\n")

    elif opcao == "3":
        print(f"\nExtrato\n{extrato}\n Saldo atual: R${saldo:.2f}")
           
    elif opcao == "4":
        print("Sair do Sistema")
        break;
