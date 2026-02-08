# Tutorial: Como Fazer Deploy no Vercel pelo Terminal

Este guia explica como colocar seu projeto online usando a Vercel CLI.

## Pré-requisitos

Você precisa ter o **Node.js** instalado para rodar o comando da Vercel.
Se não tiver, baixe em: [nodejs.org](https://nodejs.org/)

## Passo 1: Instalar a Vercel CLI

Abra o terminal e instale a ferramenta da Vercel globalmente:

```powershell
npm i -g vercel
```

## Passo 2: Login

Autentique sua máquina na sua conta Vercel:

```powershell
vercel login
```
*Siga as instruções na tela (geralmente ele abre o navegador para você autorizar).*

## Passo 3: Fazer o Deploy (Produção)

Na pasta do projeto (`c:\Users\Rafael\reddit agents`), rode:

```powershell
vercel --prod
```

### Perguntas da Instalação
O Vercel fará algumas perguntas. Responda assim:

1.  **Set up and deploy?** `Y` (Yes)
2.  **Which scope?** (Selecione sua conta pessoal)
3.  **Link to existing project?** `N` (No)
4.  **Project Name?** `reddit-intelligence-report` (ou o nome que preferir)
5.  **In which directory is your code located?** `./` (Apenas aperte Enter)
6.  **Auto-detected Project Settings (Python)?**
    *   Aqui ele pode sugerir configurações padrão.
    *   Se perguntar se quer mexer nas configurações (`Want to modify these settings?`), diga `N` (No). Nós já configuramos tudo no `vercel.json`.

## Passo 4: Verificar

Após o upload, o terminal mostrará um link de **Production**.
Algo como: `https://reddit-intelligence-report.vercel.app`

### ⚠️ Importante sobre a "Camada Gratuita"
Como usamos Python (Serverless Functions), a primeira requisição pode levar uns segundos para "acordar" o servidor ("Cold Start"). Depois disso, fica rápido.

---

## 🚀 Resumo Rápido

```powershell
npm i -g vercel
vercel login
vercel --prod
```
