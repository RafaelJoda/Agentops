# 🕵️♂️ AgentOps: Reddit Intelligence Report

Uma aplicação moderna de monitoramento de tendências para comunidades do Reddit. Este projeto utiliza uma arquitetura baseada em **Agentes** para coletar, analisar e visualizar dados de engajamento em tempo real.

## 🚀 Funcionalidades

-   **Monitoramento Multi-Tópico**: Acompanhe comunidades como `r/n8n`, `r/automation` ou adicione qualquer tópico dinamicamente (ex: `r/javascript`).
-   **Scoring de Engajamento**: Algoritmo que calcula a relevância baseada em Upvotes e Comentários.
-   **Dashboard Visual**:
    -   Gráficos de barra interativos para comparar posts.
    -   Interface *Dark Mode* com design Glassmorphism.
    -   Exibição de Thumbnails/Capas dos posts.
-   **Backend Híbrido**:
    -   Script de execução direta (`execution/`) para coleta de dados.
    -   Servidor API leve para buscas sob demanda.

## 🛠️ Tecnologias

-   **Frontend**: HTML5, CSS3 Moderno (Variaveis, Flexbox/Grid), Vanilla JavaScript, Chart.js.
-   **Backend**: Python 3.x, Requests (API do Reddit), `http.server` (Native).
-   **Dados**: Armazenamento intermediário em JSON (`.tmp/`).

## 📂 Estrutura do Projeto

```
/
├── dashboard/          # Interface Web (HTML/CSS/JS)
├── directives/         # Regras de negócio e configurações do agente
├── execution/          # Scripts Python (Scraper e Servidor)
├── logs/               # Logs detalhados de execução
└── .tmp/               # Dados processados (JSON)
```

## ▶️ Como Rodar

1.  **Instalar Dependências** (Opcional, apenas `requests` e `python-dotenv`):
    ```bash
    pip install -r requirements.txt
    ```

2.  **Iniciar o Painel**:
    ```bash
    py execution/serve_dashboard.py
    ```
    O navegador abrirá automaticamente em `http://localhost:8000/dashboard/`.

3.  **Adicionar Tópicos**:
    No topo do dashboard, digite o nome de um subreddit (ex: `python`) e clique no `+`.
