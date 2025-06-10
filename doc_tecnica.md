# Alerta Leitos

## escrição Geral

Este projeto visa fornecer um sistema de gerenciamento de leitos hospitalares com foco na organização de ocupação, liberação, controle de status (como limpeza e manutenção) e histórico dos leitos. Ele foi desenvolvido em **Python** e tem como objetivo simular uma solução que pode ser aplicada em hospitais e centros de saúde.

---

## Objetivos Técnicos

- Desenvolver lógica robusta de controle de leitos hospitalares com múltiplos estados.
- Utilizar estruturas de dados como listas e dicionários para representação de entidades e seus históricos.
- Implementar persistência de dados usando arquivos JSON, com serialização de objetos `datetime`.
- Adotar tratamento de exceções abrangente para garantir robustez e estabilidade do sistema.
- Gerenciar diferentes perfis de usuário (enfermeiro e paciente) com acesso a funcionalidades específicas.

---

## Estrutura de Dados

### Leito (dicionário)

```python
{
    "numero": "1",
    "status": "Disponível",
    "paciente": None,
    "entrada_ocupacao": None,
    "historico": [
        {
            "tipo": "mudanca_status",
            "status_anterior": "Disponível",
            "novo_status": "Ocupado",
            "timestamp": "2025-06-09T10:30:00.123456",
            "paciente": "João Silva",
            "tempo_permanencia": "2h 30min"
        }
    ]
}
```

### Credenciais (dicionários simples)

```python
ENFERMEIRO_CREDENCIAIS = {"usuario": "senha"}
PACIENTE_CREDENCIAIS = {"usuario": "senha"}
```

---

## Estrutura de Arquivos

```
projeto_leitos/
│
├── leitos.py            # Código-fonte principal
├── leitos.json          # Arquivo com os dados dos leitos
├── README.md            # Este documento
├── doc_tecnica.md       # Documento técnico detalhado
└── diagrama_uml.png     # Diagrama UML da estrutura
```

---

## Tecnologias Utilizadas

- **Linguagem:** Python 3.x  
- **Estruturas:** Listas, dicionários  
- **Módulos:** `json`, `datetime`  
- **Persistência:** Arquivo JSON  
- **Interface:** Linha de comando (CLI)

---

## Funcionalidades Implementadas

| Função                        | Descrição                                                                 |
|------------------------------|---------------------------------------------------------------------------|
| `salvar_leitos()`            | Salva os dados no arquivo JSON.                                           |
| `carregar_leitos()`          | Carrega os dados dos leitos, com tratamento de erros.                     |
| `encontrar_leito()`          | Localiza um leito específico pelo número.                                 |
| `_atualizar_status_leito()`  | Atualiza o status e registra no histórico.                                |
| `adicionar_leito()`          | Adiciona novo leito com status "Disponível".                              |
| `remover_leito()`            | Remove um leito, se não estiver ocupado.                                  |
| `ocupar_leito()`             | Ocupa um leito com paciente.                                              |
| `liberar_leito()`            | Libera um leito ocupado.                                                  |
| `iniciar_limpeza()`          | Marca leito como "Em Limpeza".                                            |
| `finalizar_limpeza()`        | Marca leito como "Leito Pronto" após limpeza.                             |
| `iniciar_manutencao()`       | Marca leito como "Em Manutenção".                                         |
| `finalizar_manutencao()`     | Marca leito como "Leito Pronto" após manutenção.                          |
| `visualizar_leitos()`        | Mostra todos os leitos ordenados numericamente.                           |
| `visualizar_leitos_ocupados()` | Lista apenas os leitos ocupados com tempo de permanência.               |
| `visualizar_historico()`     | Exibe o histórico de mudanças de status.                                  |
| `buscar_leitos()`            | Busca leitos por número, status ou paciente.                              |
| `login_usuario()`            | Valida credenciais de enfermeiro ou paciente.                             |
| `main()`                     | Executa o menu principal do sistema.                                      |

---

## Tratamento de Exceções

O sistema utiliza blocos `try-except` para:

- Garantir leitura e escrita corretas de arquivos JSON.
- Tratar entradas inválidas do usuário.
- Exibir mensagens de erro claras sem interromper o funcionamento.
- Aplicar `.strip()` e `.lower()` em entradas para evitar falhas por espaços ou capitalização.

---
## Persistência

- Os dados dos leitos são salvos automaticamente em `leitos.json`.
- Objetos `datetime` são convertidos para ISO 8601 ao salvar e reconvertidos ao carregar.
- Isso garante que o histórico de ocupações e mudanças de status seja mantido entre sessões.

---

## Diagrama UML


+---------------------------------+
|          Sistema                |
+---------------------------------+
| - leitos: list                  |
| - ENFERMEIRO_CREDENCIAIS: dict  |
| - PACIENTE_CREDENCIAIS: dict    |
+---------------------------------+
| +main()                         |
| +carregar_leitos()              |
| +salvar_leitos()                |
+---------------------------------+

        ▲
        │ usa
        ▼

+-----------------------+
|          Leito        |
+-----------------------+
| - numero: str         |
| - status: str         |
| - paciente: str       |
| - entrada_ocupacao: datetime |
| - historico: list     |
+-----------------------+
| +ocupar(paciente: str)|
| +liberar()            |
| +adicionar(numero: str)|
| +remover(numero: str) |
| +iniciar_limpeza()    |
| +finalizar_limpeza()  |
| +iniciar_manutencao() |
| +finalizar_manutencao()|
+-----------------------+

        ▲
        │ contém
        ▼

+----------------------------+
|        Historico           |
+----------------------------+
| - tipo: str                |
| - status_anterior: str     |
| - novo_status: str         |
| - timestamp: datetime      |
| - paciente: str            |
| - tempo_permanencia: str   |
+----------------------------+
```

---

## 📋 Considerações Finais

Este projeto demonstra como o Python pode ser aplicado para resolver desafios práticos na área da saúde. A modularização do código, a persistência de dados e a separação de perfis de usuário tornam a solução facilmente expansível para:

- Interfaces gráficas (GUI)
- Integração com banco de dados
- Sistemas em tempo real com notificações

---

## ✅ Status do Projeto

✅ Concluído – Pronto para testes e melhorias futuras!

---

## 👨‍⚕️ Desenvolvido por

> Henrique, Davis, Jonathan, Alan e Lucas
