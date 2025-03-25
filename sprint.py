# Função para adicionar um leito
def adicionar_leito(leitos, numero):
    leito = {"numero": numero, "ocupado": False, "paciente": None}
    leitos.append(leito)
    print(f"Leito {numero} adicionado.")

# Função para ocupar um leito
def ocupar_leito(leitos, numero, paciente):
    for leito in leitos:
        if leito["numero"] == numero:
            if not leito["ocupado"]:
                leito["ocupado"] = True
                leito["paciente"] = paciente
                print(f"Leito {numero} ocupado por {paciente}.")
            else:
                print(f"Leito {numero} já está ocupado.")
            return
    print(f"Leito {numero} não encontrado.")

# Função para liberar um leito
def liberar_leito(leitos, numero):
    for leito in leitos:
        if leito["numero"] == numero:
            if leito["ocupado"]:
                leito["ocupado"] = False
                leito["paciente"] = None
                print(f"Leito {numero} liberado.")
            else:
                print(f"Leito {numero} já está disponível.")
            return
    print(f"Leito {numero} não encontrado.")

# Função para visualizar os leitos
def visualizar_leitos(leitos):
    print("Status dos Leitos:")
    for leito in leitos:
        status = "Ocupado" if leito["ocupado"] else "Disponível"
        paciente_info = f" - Paciente: {leito['paciente']}" if leito["ocupado"] else ""
        print(f"Leito {leito['numero']}: {status}{paciente_info}")

# Função para visualizar leitos ocupados
def visualizar_leitos_ocupados(leitos):
    print("Leitos Ocupados:")
    ocupados = [leito for leito in leitos if leito["ocupado"]]
    if not ocupados:
        print("Nenhum leito ocupado.")
    else:
        for leito in ocupados:
            print(f"Leito {leito['numero']} - Paciente: {leito['paciente']}")
            
# Função principal
def main():
    leitos = []
    # Adicionando 10 leitos padrão
    for i in range(1, 11):
        adicionar_leito(leitos, str(i)) 
    print("\nLeitos adicionados:")

    for leito in leitos:
        print(f"Leito {leito['numero']} - Ocupado: {leito['ocupado']}")
    while True:
        print("\nMenu:")
        print("1. Adicionar Leito")
        print("2. Ocupação de Leito")
        print("3. Liberação de Leito")
        print("4. Visualizar Leitos")
        print("5. Visualizar Leitos Ocupados")
        print("6. Sair")
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            numero = input("Digite o número do leito: ")
            adicionar_leito(leitos, numero)
        elif opcao == '2':
            numero = input("Digite o número do leito: ")
            paciente = input("Digite o nome do paciente: ")
            ocupar_leito(leitos, numero, paciente)
        elif opcao == '3':
            numero = input("Digite o número do leito: ")
            liberar_leito(leitos, numero)
        elif opcao == '4':
            visualizar_leitos(leitos)
         elif opcao == '5':
            visualizar_leitos_ocupados(leitos)
        elif opcao == '6':
            print("Saindo do sistema.")
            break
        else:
            print("Opção inválida. Tente novamente.")
if __name__ == "__main__":
    main()
