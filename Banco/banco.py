from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    

    def sacar(self, valor):
        saldo = self.saldo
        
        if valor > saldo:
            print("\nSaldo Insuficiente!")

        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso!")
            return True
        else:
            print("\nValor inválido")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n Depósito realizado com sucesso!")
        else:
            print("\nValor informado é inválido.")
            return False

        return True
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques= limite_saques

    def sacar(self, valor):
        numero_saque = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
                           )
        
        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saque >= self._limite_saques

        if excedeu_limite:
            print(f"\nO valor do saque está acima do limite")

        elif excedeu_saques:
            print(f"\nNumero maximo de saques atingido")

        else:
            return super().sacar(valor)

        return False
    
    def __str__(self):
        return (f"""\
            Agencia: {self.agencia}
            Conta Corrente: {self.numero}
            Titular: {self.cliente.nome}
        """)

class Historico:
    def __init__(self) -> None:
        self._transacoes =[] 

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "transacao": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y, %H:%M:%S"),
        })

class Transacao(ABC):
    
    @property
    @abstractmethod 
    def valor(self):
        pass
    
    @property
    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):

    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor) #recebe TRUE

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    menu = """
    --- MENU --- 

    1 - Saque
    2 - Depósito
    3 - Extrato
    4 - Criar Conta Corrente 
    5 - Criar Cliente
    6 - Listar Conta Corrente
    7 - Sair

    Digite a opção escolhida: """

    return input(textwrap.dedent(menu)) 

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente nao possui conta!")
        return
    
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Digite o CPF: ")
    cliente = filtrar_cpf(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    valor = float(input("Valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Digite o CPF: ")
    cliente = filtrar_cpf(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    valor = float(input("Valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def func_extrato(clientes):
    cpf = input("CPF do cliente: ")
    cliente = filtrar_cpf(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\t === EXTRATO ===")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Nenhuma movimentação!"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")    

def criar_cc(numero_conta, clientes, contas):
    cpf = input("CPF do cliente: ")
    cliente = filtrar_cpf(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\nConta criada com sucesso!")

def criar_cliente(clientes):
    cpf = input("Entre com o CPF:" )
    cliente = filtrar_cpf(cpf, clientes)

    if cliente:
        print("\nCliente já existe!")
        return 

    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\nCliente Criado!")

def listar_cc(contas):
    for conta in contas:
        print("=" * 20)
        print(textwrap.dedent(str(conta)))

def filtrar_cpf(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def main():
    clientes = []
    contas = []

    print(
        '''\n --- Sistema de Banco --- \n'''
        )

    while True:

        opcao = menu()

        if opcao == "1":
            print("\n--- Saque ---")
            sacar(clientes)
            
        elif opcao == "2":
            print("\n--- Depósito ---")
            depositar(clientes)

        elif opcao == "3":
            print("\n--- Extrato ---")
            func_extrato(clientes)

        elif opcao == "4":
            print("\n--- Criar Conta Corrente ---")
            numero_conta = len(contas) + 1   
            criar_cc(numero_conta, clientes, contas)
                    
        elif opcao == "5":
            print("\n--- Criar Cliente ---") 
            criar_cliente(clientes)

        elif opcao == "6":
            print("\n--- Listar Todas as Contas Correntes ---")
            listar_cc(contas)

        elif opcao == "7":
            print("Sair do Sistema")
            break;

#para execução
main()