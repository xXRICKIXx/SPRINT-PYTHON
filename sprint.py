import json

# Função para salvar os dados dos leitos
def salvar_leitos(leitos, arquivo="leitos.json"):
    try:
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(leitos, f, ensure_ascii=False, indent=4)
        print("Dados salvos com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")

# Função para carregar os dados dos leitos
def carregar_leitos(arquivo="leitos.json"):
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Arquivo não encontrado. Iniciando com lista de leitos vazia.")
        return []
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return []

# Função para adicionar um leito
def adicionar_leito(leitos, numero):
    leito = {"numero": numero, "ocupado": False, "paciente": None, "historico": []}
    leitos.append(leito)
    print(f"Leito {numero} adicionado.")

# Função para ocupar um leito
def ocupar_leito(leitos, numero, paciente):
    for leito in leitos:
        if leito["numero"] == numero:
            if not leito["ocupado"]:
                leito["ocupado"] = True
                leito["paciente"] = paciente
                leito["historico"].append({"paciente": paciente, "tempo": "agora"})  # Substituir por datetime se quiser
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
    print("\nStatus dos Leitos:")
    for leito in leitos:
        status = "Ocupado" if leito["ocupado"] else "Disponível"
        paciente_info = f" - Paciente: {leito['paciente']}" if leito["ocupado"] else ""
        print(f"Leito {leito['numero']}: {status}{paciente_info}")

# Função para visualizar leitos ocupados
def visualizar_leitos_ocupados(leitos):
    print("\nLeitos Ocupados:")
    ocupados = [leito for leito in leitos if leito["ocupado"]]
    if not ocupados:
        print("Nenhum leito ocupado.")
    else:
        for leito in ocupados:
            print(f"Leito {leito['numero']} - Paciente: {leito['paciente']}")

# Função para visualizar histórico de ocupação
def visualizar_historico(leitos):
    print("\nHistórico de Leitos:")
    for leito in leitos:
        print(f"\nLeito {leito['numero']}:")
        if leito["historico"]:
            for h in leito["historico"]:
                print(f"  Paciente: {h['paciente']} - Tempo: {h['tempo']}")
        else:
            print("  Nenhum histórico registrado.")

# Função de login
def login_usuario(tipo):
    usuario = input(f"Digite o nome do {tipo}: ")
    senha = input(f"Digite a senha do {tipo}: ")
    print(f"{tipo.capitalize()} {usuario} logado com sucesso.")
    return usuario

# Função principal
def main():
    leitos = carregar_leitos()

    if not leitos:
        for i in range(1, 11):
            adicionar_leito(leitos, str(i))

    tipo_usuario = input("\nVocê é um paciente ou enfermeiro? (digite 'paciente' ou 'enfermeiro'): ").lower()
    if tipo_usuario not in ['paciente', 'enfermeiro']:
        print("Tipo de usuário inválido. Saindo.")
        return

    usuario_logado = login_usuario(tipo_usuario)

    while True:
        print("\nMenu:")
        if tipo_usuario == 'enfermeiro':
            print("1. Adicionar Leito")
            print("2. Ocupação de Leito")
            print("3. Liberação de Leito")
        print("4. Visualizar Leitos")
        print("5. Visualizar Leitos Ocupados")
        print("6. Visualizar Histórico de Leitos")
        print("7. Sair")

        opcao = input("Escolha uma opção: ")

        try:
            if tipo_usuario == 'enfermeiro':
                if opcao == '1':
                    numero = input("Digite o número do novo leito: ")
                    adicionar_leito(leitos, numero)
                elif opcao == '2':
                    numero = input("Digite o número do leito a ser ocupado: ")
                    paciente = input("Digite o nome do paciente: ")
                    ocupar_leito(leitos, numero, paciente)
                elif opcao == '3':
                    numero = input("Digite o número do leito a ser liberado: ")
                    liberar_leito(leitos, numero)
                elif opcao == '4':
                    visualizar_leitos(leitos)
                elif opcao == '5':
                    visualizar_leitos_ocupados(leitos)
                elif opcao == '6':
                    visualizar_historico(leitos)
                elif opcao == '7':
                    salvar_leitos(leitos)
                    print("Saindo do sistema...")
                    break
                else:
                    print("Opção inválida. Tente novamente.")
            else:  # paciente
                if opcao == '4':
                    visualizar_leitos(leitos)
                elif opcao == '5':
                    visualizar_leitos_ocupados(leitos)
                elif opcao == '6':
                    visualizar_historico(leitos)
                elif opcao == '7':
                    salvar_leitos(leitos)
                    print("Saindo do sistema...")
                    break
                else:
                    print("Opção inválida. Tente novamente.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

# Executa o sistema
if __name__ == "__main__":
    main()
