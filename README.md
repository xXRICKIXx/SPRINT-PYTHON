# Sistema de Gerenciamento de Leitos Hospitalares

## 🏥 Sobre o Projeto

Este é um protótipo funcional desenvolvido em Python para gerenciar a ocupação de leitos hospitalares. O sistema permite a adição, ocupação, liberação e visualização de leitos, bem como o histórico de uso. Usuários podem acessar o sistema como **enfermeiros** ou **pacientes**, com permissões distintas para cada tipo.

## 🎯 Objetivos

- Demonstrar o uso de **estruturas de dados** como listas e dicionários;
- Implementar **manipulação de arquivos** para salvar e carregar os dados dos leitos;
- Garantir robustez com **tratamento de exceções**;
- Apresentar uma interface simples em linha de comando;
- Promover o pensamento computacional aplicado a contextos reais da área da saúde.

## 🧩 Funcionalidades

### Para Enfermeiros:
- Adicionar novo leito
- Ocupar um leito com nome do paciente
- Liberar um leito
- Visualizar todos os leitos
- Ver apenas os leitos ocupados
- Acessar histórico de ocupação dos leitos

### Para Pacientes:
- Visualizar todos os leitos
- Ver apenas os leitos ocupados
- Acessar histórico de ocupação

## 🧠 Tecnologias Utilizadas

- **Python 3.x**
- Estruturas de dados: listas, dicionários
- Manipulação de arquivos `.json`
- Tratamento de exceções (`try/except`)
- Interface CLI (Command Line Interface)

## 📂 Estrutura do Projeto

```
projeto_leitos/
│
├── leitos.py            # Código principal do sistema
├── leitos.json          # Arquivo gerado com os dados salvos
├── README.md            # Este arquivo
└── diagrama_uml.png     # Diagrama de classes do sistema
```

## 📌 Como Executar

1. Certifique-se de ter o Python instalado:
   ```bash
   python --version
   ```

2. Execute o script principal:
   ```bash
   python sprint.py
   ```

3. Siga as instruções exibidas no terminal.

## 📈 Diagrama de Classes
+------------------+
|     Sistema      |
+------------------+
| - leitos: list   |
+------------------+
| +main()          |
| +carregar_leitos()|
| +salvar_leitos()  |
+------------------+

        ▲
        │
        │ usa
        ▼

+-------------------+
|     Leito         |
+-------------------+
| - numero: str     |
| - ocupado: bool   |
| - paciente: str   |
| - historico: list |
+-------------------+
| +ocupar(paciente) |
| +liberar()        |
| +adicionar()      |
+-------------------+

        ▲
        │
        │ contém
        ▼

+-------------------+
|   Historico       |
+-------------------+
| - paciente: str   |
| - tempo: str      |
+-------------------+


## 👥 Equipe

- Henrique Celso 
- Jonathan Henrique 
- Davis Jr 
- Alan de Castro 
- Lucas Cortizo


