import json
from datetime import datetime, timedelta

# Credenciais de exemplo (em caso de um sistema real, isso viria de um banco de dados seguro)
ENFERMEIRO_CREDENCIAIS = {"enfermeiro1": "senha123", "enfermeiro2": "abcd"}
PACIENTE_CREDENCIAIS = {"paciente1": "1234", "paciente2": "efgh"}


# Funções de persistência de dados

def salvar_leitos(leitos, arquivo="leitos.json"):
    """
    Salva os dados dos leitos em um arquivo JSON.
    Converte objetos datetime para string ISO format para compatibilidade JSON.
    """
    try:
        # Cria uma cópia profunda para evitar modificar a lista original
        leitos_para_salvar = []
        for leito in leitos:
            leito_copia = leito.copy()
            if leito_copia.get("entrada_ocupacao"):
                leito_copia["entrada_ocupacao"] = leito_copia["entrada_ocupacao"].isoformat()

            # Converte timestamps do histórico
            historico_copia = []
            for h in leito_copia["historico"]:
                h_copia = h.copy()
                if isinstance(h_copia.get("timestamp"), datetime):
                    h_copia["timestamp"] = h_copia["timestamp"].isoformat()
                historico_copia.append(h_copia)
            leito_copia["historico"] = historico_copia
            leitos_para_salvar.append(leito_copia)

        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(leitos_para_salvar, f, ensure_ascii=False, indent=4)
        print("Dados salvos com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")


def carregar_leitos(arquivo="leitos.json"):
    """Carrega os dados dos leitos de um arquivo JSON.
    Converte strings ISO format de volta para objetos datetime."""
   
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            leitos_carregados = json.load(f)
            # Converte strings de volta para objetos datetime
            for leito in leitos_carregados:
                if leito.get("entrada_ocupacao") and isinstance(leito["entrada_ocupacao"], str):
                    leito["entrada_ocupacao"] = datetime.fromisoformat(leito["entrada_ocupacao"])
                for h in leito["historico"]:
                    if h.get("timestamp") and isinstance(h["timestamp"], str):
                        h["timestamp"] = datetime.fromisoformat(h["timestamp"])
            return leitos_carregados
    except FileNotFoundError:
        print("Arquivo não encontrado. Iniciando com lista de leitos vazia.")
        return []
    except json.JSONDecodeError:
        print("Erro ao decodificar JSON. O arquivo pode estar corrompido. Iniciando com lista vazia.")
        return []
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return []


# Funções de manipulação de leitos 

def encontrar_leito(leitos, numero):
    """Auxiliar para encontrar um leito pelo número."""
    for leito in leitos:
        # Garante que a comparação seja entre strings
        if str(leito["numero"]) == str(numero):
            return leito
    return None


def _atualizar_status_leito(leito, novo_status, paciente=None):
    """Função auxiliar para atualizar o status do leito e registrar no histórico."""
   
    status_anterior = leito["status"]

    # Lógica para registrar no histórico antes de mudar o status
    historico_entry = {
        "tipo": "mudanca_status",
        "status_anterior": status_anterior,
        "novo_status": novo_status,
        "timestamp": datetime.now()
    }

    leito["status"] = novo_status

    if novo_status == "Ocupado":
        leito["paciente"] = paciente
        leito["entrada_ocupacao"] = datetime.now()
        historico_entry["paciente"] = paciente  # Adiciona paciente ao registro de entrada
        print(f"Leito {leito['numero']} agora está {novo_status} por {paciente}.")
    elif novo_status in ["Disponível", "Leito Pronto"]:
        # Se estava ocupado e agora está disponível/pronto, registra saída
        if status_anterior == "Ocupado":
            agora = datetime.now()
            tempo_permanencia = agora - leito["entrada_ocupacao"]
            horas, minutos = divmod(tempo_permanencia.total_seconds(), 3600)
            minutos, segundos = divmod(minutos, 60)
            permanencia_formatada = f"{int(horas)}h {int(minutos)}min"
            if int(segundos) > 0:
                permanencia_formatada += f" {int(segundos)}s"

            historico_entry["paciente"] = leito["paciente"]  # Registra paciente que saiu
            historico_entry["tempo_permanencia"] = permanencia_formatada

            leito["paciente"] = None
            leito["entrada_ocupacao"] = None
            print(
                f"Leito {leito['numero']} agora está {novo_status}. Paciente {historico_entry['paciente']} permaneceu por {permanencia_formatada}.")
        else:
            leito["paciente"] = None
            leito["entrada_ocupacao"] = None
            print(f"Leito {leito['numero']} agora está {novo_status}.")
    else:  # Outros status como "Em Limpeza", "Em Manutenção"
        leito["paciente"] = None  # Não tem paciente nesses estados
        leito["entrada_ocupacao"] = None  # Não tem entrada de ocupação nesses estados
        print(f"Leito {leito['numero']} agora está {novo_status}.")

    leito["historico"].append(historico_entry)


def adicionar_leito(leitos, numero):
    """Adiciona um novo leito à lista com status 'Disponível'."""
    # Garante que o número seja tratado como string ao adicionar
    numero_str = str(numero).strip()
    if encontrar_leito(leitos, numero_str):
        print(f"Erro: Leito {numero_str} já existe.")
        return
    leito = {"numero": numero_str, "status": "Disponível", "paciente": None, "entrada_ocupacao": None, "historico": []}
    leitos.append(leito)
    leitos.sort(key=lambda x: int(x["numero"]))  # Mantém a lista ordenada por número
    print(f"Leito {numero_str} adicionado.")


def remover_leito(leitos, numero):
    """Remove um leito existente, se não estiver ocupado."""
    numero_str = str(numero).strip() # Garante que o número seja tratado como string
    leito = encontrar_leito(leitos, numero_str)
    if leito:
        confirmacao = input(f"Tem certeza que deseja remover o leito {numero_str}? (s/n): ").lower().strip()
        if confirmacao == 's':
            if leito["status"] == "Ocupado":
                print(f"Erro: Leito {numero_str} está ocupado. Libere-o antes de remover.")
            else:
                leitos.remove(leito)
                print(f"Leito {numero_str} removido com sucesso.")
        else:
            print("Remoção de leito cancelada.")
    else:
        print(f"Leito {numero_str} não encontrado.")


def ocupar_leito(leitos, numero, paciente):
    """Ocupa um leito com um paciente."""
    numero_str = str(numero).strip() # Garante que o número seja tratado como string
    leito = encontrar_leito(leitos, numero_str)
    if leito:
        if leito["status"] in ["Disponível", "Leito Pronto"]:
            _atualizar_status_leito(leito, "Ocupado", paciente)
        else:
            print(f"Leito {numero_str} não está disponível para ocupação. Status atual: {leito['status']}.")
        return
    print(f"Leito {numero_str} não encontrado.")


def liberar_leito(leitos, numero):
    """Libera um leito ocupado e registra o tempo de permanência."""
    numero_str = str(numero).strip() # Garante que o número seja tratado como string
    leito = encontrar_leito(leitos, numero_str)
    if leito:
        if leito["status"] == "Ocupado":
            _atualizar_status_leito(leito, "Leito Pronto", leito["paciente"])  # Passa o nome do paciente para registro
        else:
            print(f"Leito {numero_str} não está ocupado. Status atual: {leito['status']}.")
        return
    print(f"Leito {numero_str} não encontrado.")


def iniciar_limpeza(leitos, numero):
    """Altera o status do leito para 'Em Limpeza'."""
    numero_str = str(numero).strip() # Garante que o número seja tratado como string
    leito = encontrar_leito(leitos, numero_str)
    if leito:
        if leito["status"] in ["Disponível", "Leito Pronto"]:
            _atualizar_status_leito(leito, "Em Limpeza")
        else:
            print(f"Leito {numero_str} não pode iniciar limpeza. Status atual: {leito['status']}.")
        return
    print(f"Leito {numero_str} não encontrado.")


def finalizar_limpeza(leitos, numero):
    """Altera o status do leito de 'Em Limpeza' para 'Leito Pronto'."""
    numero_str = str(numero).strip() # Garante que o número seja tratado como string
    leito = encontrar_leito(leitos, numero_str)
    if leito:
        if leito["status"] == "Em Limpeza":
            _atualizar_status_leito(leito, "Leito Pronto")
        else:
            print(f"Leito {numero_str} não está em limpeza. Status atual: {leito['status']}.")
        return
    print(f"Leito {numero_str} não encontrado.")


def iniciar_manutencao(leitos, numero):
    """Altera o status do leito para 'Em Manutenção'."""
    numero_str = str(numero).strip() # Garante que o número seja tratado como string
    leito = encontrar_leito(leitos, numero_str)
    if leito:
        if leito["status"] in ["Disponível", "Leito Pronto"]:
            _atualizar_status_leito(leito, "Em Manutenção")
        else:
            print(f"Leito {numero_str} não pode iniciar manutenção. Status atual: {leito['status']}.")
        return
    print(f"Leito {numero_str} não encontrado.")


def finalizar_manutencao(leitos, numero):
    """Altera o status do leito de 'Em Manutenção' para 'Leito Pronto'."""
    numero_str = str(numero).strip() # Garante que o número seja tratado como string
    leito = encontrar_leito(leitos, numero_str)
    if leito:
        if leito["status"] == "Em Manutenção":
            _atualizar_status_leito(leito, "Leito Pronto")
        else:
            print(f"Leito {numero_str} não está em manutenção. Status atual: {leito['status']}.")
        return
    print(f"Leito {numero_str} não encontrado.")


# Funções de visualização 

def visualizar_leitos(leitos):
    """Exibe o status atual de todos os leitos."""
    print("\n--- Status dos Leitos ---")
    if not leitos:
        print("Nenhum leito cadastrado.")
        return

    # Garante que os leitos sejam exibidos em ordem numérica
    leitos_ordenados = sorted(leitos, key=lambda x: int(x['numero']))

    for leito in leitos_ordenados:
        status = leito["status"]
        paciente_info = ""
        tempo_info = ""
        if leito["status"] == "Ocupado" and leito["entrada_ocupacao"]:
            paciente_info = f" - Paciente: {leito['paciente']}"
            agora = datetime.now()
            tempo_decorrido = agora - leito["entrada_ocupacao"]
            horas, minutos = divmod(tempo_decorrido.total_seconds(), 3600)
            tempo_info = f" (há {int(horas)}h {int(minutos)}min)"

        print(f"Leito {leito['numero']}: {status}{paciente_info}{tempo_info}")


def visualizar_leitos_ocupados(leitos):
    """Exibe apenas os leitos atualmente ocupados, com tempo de permanência."""
    print("\n--- Leitos Ocupados ---")
    ocupados = [leito for leito in leitos if leito["status"] == "Ocupado"]
    if not ocupados:
        print("Nenhum leito ocupado no momento.")
    else:
        # Garante que os leitos ocupados sejam exibidos em ordem numérica
        ocupados_ordenados = sorted(ocupados, key=lambda x: int(x['numero']))
        for leito in ocupados_ordenados:
            agora = datetime.now()
            tempo_decorrido = agora - leito["entrada_ocupacao"]
            horas, minutos = divmod(tempo_decorrido.total_seconds(), 3600)
            print(f"Leito {leito['numero']} - Paciente: {leito['paciente']} (Há {int(horas)}h {int(minutos)}min)")


def visualizar_historico(leitos):
    """Exibe o histórico detalhado de ocupação e liberação/mudanças de status de cada leito."""
    print("\n--- Histórico de Leitos ---")
    if not leitos:
        print("Nenhum leito cadastrado para histórico.")
        return

    # Garante que os leitos sejam exibidos em ordem numérica
    leitos_ordenados = sorted(leitos, key=lambda x: int(x['numero']))

    for leito in leitos_ordenados:
        print(f"\nLeito {leito['numero']}:")
        if leito["historico"]:
            for h in leito["historico"]:
                timestamp_str = h["timestamp"].strftime('%d/%m/%Y %H:%M:%S')
                msg = f"  Status alterado de '{h['status_anterior']}' para '{h['novo_status']}' em: {timestamp_str}"
                if h.get("paciente"):
                    msg += f" (Paciente: {h['paciente']})"
                if h.get("tempo_permanencia"):
                    msg += f" (Permanência: {h['tempo_permanencia']})"
                print(msg)
        else:
            print("  Nenhum histórico registrado.")


def buscar_leitos(leitos):
    """Permite buscar leitos por número, status ou nome do paciente."""
    print("\n--- Buscar Leitos ---")
    criterio = input("Buscar por (número/status/paciente): ").strip().lower()
    resultados = []

    if criterio == "numero":
        num_busca = input("Digite o número do leito: ").strip()
        if not num_busca.isdigit():
            print("Número de leito inválido.")
            return
        leito = encontrar_leito(leitos, num_busca) # num_busca já é string e limpo
        if leito:
            resultados.append(leito)
    elif criterio == "status":
        status_busca = input("Digite o status (Disponível, Ocupado, Em Limpeza, Em Manutenção, Leito Pronto): ").strip()
        resultados = [leito for leito in leitos if leito["status"].lower() == status_busca.lower()]
    elif criterio == "paciente":
        paciente_busca = input("Digite o nome do paciente: ").strip().lower()
        resultados = [leito for leito in leitos if
                      leito["paciente"] and paciente_busca in leito["paciente"].lower()]
    else:
        print("Critério de busca inválido.")
        return

    if resultados:
        print("\n--- Resultados da Busca ---")
        resultados_ordenados = sorted(resultados, key=lambda x: int(x['numero']))
        for leito in resultados_ordenados:
            status = leito["status"]
            paciente_info = f" - Paciente: {leito['paciente']}" if leito["paciente"] else ""
            tempo_info = ""
            if leito["status"] == "Ocupado" and leito["entrada_ocupacao"]:
                agora = datetime.now()
                tempo_decorrido = agora - leito["entrada_ocupacao"]
                horas, minutos = divmod(tempo_decorrido.total_seconds(), 3600)
                tempo_info = f" (há {int(horas)}h {int(minutos)}min)"
            print(f"Leito {leito['numero']}: {status}{paciente_info}{tempo_info}")
    else:
        print("Nenhum leito encontrado com o critério especificado.")


# Funções de autenticação

def login_usuario():
    """Realiza o processo de login e retorna o tipo de usuário e nome."""
    while True:
        tipo = input("Você é um paciente ou enfermeiro? (digite 'paciente' ou 'enfermeiro'): ").lower().strip()
        if tipo not in ['paciente', 'enfermeiro']:
            print("Tipo de usuário inválido. Por favor, digite 'paciente' ou 'enfermeiro'.")
            continue

        usuario = input(f"Digite seu nome de usuário como {tipo}: ").strip()
        senha = input(f"Digite sua senha: ").strip()

        if tipo == 'enfermeiro':
            if usuario in ENFERMEIRO_CREDENCIAIS and ENFERMEIRO_CREDENCIAIS[usuario] == senha:
                print(f"Enfermeiro {usuario} logado com sucesso!")
                return tipo, usuario
            else:
                print("Nome de usuário ou senha de enfermeiro inválidos.")
        elif tipo == 'paciente':
            if usuario in PACIENTE_CREDENCIAIS and PACIENTE_CREDENCIAIS[usuario] == senha:
                print(f"Paciente {usuario} logado com sucesso!")
                return tipo, usuario
            else:
                print("Nome de usuário ou senha de paciente inválidos.")
        print("Tente novamente.")


# Função principal

def main():
    leitos = carregar_leitos()

    # Inicializa alguns leitos se o arquivo estiver vazio
    if not leitos:
        print("Inicializando leitos padrão (1 a 10)...")
        for i in range(1, 11):
            adicionar_leito(leitos, str(i)) # Garante que o número seja string
        salvar_leitos(leitos)  # Salva os leitos iniciais

    tipo_usuario, usuario_logado = login_usuario()

    while True:
        print("\n--- Menu Principal ---")
        if tipo_usuario == 'enfermeiro':
            print("1. Adicionar Leito")
            print("2. Remover Leito")
            print("3. Ocupar Leito")
            print("4. Liberar Leito")
            print("5. Iniciar Limpeza de Leito")
            print("6. Finalizar Limpeza de Leito")
            print("7. Iniciar Manutenção de Leito")
            print("8. Finalizar Manutenção de Leito")
            print("9. Buscar Leitos")
            print("10. Visualizar Todos os Leitos")
            print("11. Visualizar Leitos Ocupados")
            print("12. Visualizar Histórico de Leitos")
            print("13. Sair")
        else:  # Usuário paciente
            print("1. Buscar Leitos")
            print("2. Visualizar Todos os Leitos")
            print("3. Visualizar Leitos Ocupados")
            print("4. Visualizar Histórico de Leitos")
            print("5. Sair")

        opcao = input("Escolha uma opção: ").strip().lower()

        try:
            if tipo_usuario == 'enfermeiro':
                if opcao == '1':
                    numero = input("Digite o número do novo leito: ").strip()
                    if numero.isdigit():
                        adicionar_leito(leitos, numero)
                    else:
                        print("Número de leito inválido. Por favor, digite apenas dígitos.")
                elif opcao == '2':
                    numero = input("Digite o número do leito a ser removido: ").strip()
                    if numero.isdigit():
                        remover_leito(leitos, numero)
                    else:
                        print("Número de leito inválido. Por favor, digite apenas dígitos.")
                elif opcao == '3':
                    numero = input("Digite o número do leito a ser ocupado: ").strip()
                    paciente = input("Digite o nome do paciente: ").strip()
                    if numero.isdigit() and paciente:
                        ocupar_leito(leitos, numero, paciente)
                    else:
                        print("Entrada inválida. Verifique o número do leito e o nome do paciente.")
                elif opcao == '4':
                    numero = input("Digite o número do leito a ser liberado: ").strip()
                    if numero.isdigit():
                        liberar_leito(leitos, numero)
                    else:
                        print("Número de leito inválido. Por favor, digite apenas dígitos.")
                elif opcao == '5':
                    numero = input("Digite o número do leito para iniciar a limpeza: ").strip()
                    if numero.isdigit():
                        iniciar_limpeza(leitos, numero)
                    else:
                        print("Número de leito inválido. Por favor, digite apenas dígitos.")
                elif opcao == '6':
                    numero = input("Digite o número do leito para finalizar a limpeza: ").strip()
                    if numero.isdigit():
                        finalizar_limpeza(leitos, numero)
                    else:
                        print("Número de leito inválido. Por favor, digite apenas dígitos.")
                elif opcao == '7':
                    numero = input("Digite o número do leito para iniciar a manutenção: ").strip()
                    if numero.isdigit():
                        iniciar_manutencao(leitos, numero)
                    else:
                        print("Número de leito inválido. Por favor, digite apenas dígitos.")
                elif opcao == '8':
                    numero = input("Digite o número do leito para finalizar a manutenção: ").strip()
                    if numero.isdigit():
                        finalizar_manutencao(leitos, numero)
                    else:
                        print("Número de leito inválido. Por favor, digite apenas dígitos.")
                elif opcao == '9':
                    buscar_leitos(leitos)
                elif opcao == '10':
                    visualizar_leitos(leitos)
                elif opcao == '11':
                    visualizar_leitos_ocupados(leitos)
                elif opcao == '12':
                    visualizar_historico(leitos)
                elif opcao == '13':
                    salvar_leitos(leitos)
                    print("Saindo do sistema...")
                    break
                else:
                    print("Opção inválida. Tente novamente.")
            else:  # Usuário paciente
                if opcao == '1':
                    buscar_leitos(leitos)
                elif opcao == '2':
                    visualizar_leitos(leitos)
                elif opcao == '3':
                    visualizar_leitos_ocupados(leitos)
                elif opcao == '4':
                    visualizar_historico(leitos)
                elif opcao == '5':
                    salvar_leitos(leitos)
                    print("Saindo do sistema...")
                    break
                else:
                    print("Opção inválida. Tente novamente.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")


if __name__ == "__main__":
    main()
