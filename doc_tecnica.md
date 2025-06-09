# 🛠️ Documentação Técnica – Sistema de Gerenciamento de Leitos Hospitalares

## 📘 Descrição Geral

Este projeto visa fornecer um sistema de gerenciamento de leitos hospitalares com foco na organização de ocupação, liberação e histórico dos leitos. Ele foi desenvolvido em Python e tem como objetivo simular uma solução que pode ser aplicada em hospitais e centros de saúde.

## 🎯 Objetivos Técnicos

- Desenvolver lógica de controle de leitos hospitalares;
- Utilizar estruturas de dados como listas e dicionários;
- Implementar persistência de dados usando arquivos JSON;
- Adotar tratamento de exceções para garantir robustez.

---

## 📦 Estrutura de Dados

### Leito (Dicionário):
```python
{
    "numero": "1",
    "ocupado": False,
    "paciente": None,
    "historico": [
        {"paciente": "João", "tempo": "2025-06-09 10:30:00"}
    ]
}
```

## 📂 Estrutura de Arquivos

```
projeto_leitos/
│
├── leitos.py            # Código-fonte principal
├── leitos.json          # Arquivo com os dados salvos dos leitos
├── README.md            # Apresentação geral do projeto
├── doc_tecnica.md       # Este documento
└── diagrama_uml.png     # Diagrama UML da estrutura
```

---

## 🧠 Tecnologias Utilizadas

- Linguagem: Python 3.x
- Estruturas: Listas, dicionários
- Módulos: `json`, `datetime`
- Persistência: Arquivo JSON
- Interface: Linha de comando (CLI)

---

## 📌 Funcionalidades Implementadas

| Função                         | Descrição |
|-------------------------------|-----------|
| `adicionar_leito()`           | Cria um novo leito |
| `ocupar_leito()`              | Ocupa um leito com nome de paciente |
| `liberar_leito()`             | Libera um leito ocupado |
| `visualizar_leitos()`         | Mostra todos os leitos e seus status |
| `visualizar_leitos_ocupados()`| Lista somente os leitos ocupados |
| `visualizar_historico()`      | Exibe o histórico de ocupações de cada leito |
| `login_usuario()`             | Simula login de paciente ou enfermeiro |
| `main()`                      | Executa o fluxo principal com menu interativo |

---

## 🧪 Tratamento de Exceções

O sistema utiliza blocos `try-except` para:

- Garantir que arquivos sejam lidos corretamente;
- Evitar falhas em entradas inválidas de usuário;
- Manter o sistema funcionando mesmo com erros pontuais.

---

## 💾 Persistência

Ao iniciar e finalizar o sistema, os dados dos leitos são salvos e carregados automaticamente do arquivo `leitos.json`. Isso permite continuidade no uso do sistema mesmo após encerramento.

---

## 📊 Diagrama UML

O diagrama de classes foi desenvolvido para representar a estrutura do sistema:

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


---

## 📋 Considerações Finais

Este projeto é um exemplo de como Python pode ser aplicado em soluções práticas no setor da saúde. A modularização, o uso de arquivos e o foco em dados estruturados permitem que o sistema seja facilmente expandido ou integrado com tecnologias como interfaces gráficas ou bancos de dados.