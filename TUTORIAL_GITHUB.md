# Tutorial: Como Subir o Projeto para o GitHub

Este guia explica passo a passo como enviar seu código local (`reddit agents`) para o repositório remoto que você criou (`Agentops`).

## Passo 1: Limpeza (Se necessário)
Como você rodou um `git clone` dentro da pasta do projeto, pode ter sido criada uma pasta vazia chamada `Agentops`. Vamos removê-la para não duplicar coisas.

```powershell
Remove-Item -Recurse -Force Agentops
```

## Passo 2: Inicializar o Git
Transforme a pasta atual em um repositório Git.

```powershell
git init
```

## Passo 3: Configurar o `.gitignore`
Garanta que arquivos sensíveis ou temporários não subam (já configuramos isso, mas é bom conferir). O arquivo `.gitignore` deve conter:
- `.env`
- `.tmp/`
- `__pycache__/`
- `logs/`

## Passo 4: Adicionar os Arquivos
Adicione todos os arquivos do projeto ao Git.

```powershell
git add .
```

## Passo 5: Criar o Primeiro Commit
Salve o estado atual do projeto.

```powershell
git commit -m "Primeira versao: Reddit Agent Dashboard com graficos e topicos dinamicos"
```

## Passo 6: Renomear Branch Principal
O padrão moderno é usar `main` em vez de `master`.

```powershell
git branch -M main
```

## Passo 7: Conectar ao GitHub
Adicione o link do seu repositório remoto.

```powershell
git remote add origin https://github.com/RafaelJoda/Agentops.git
```

## Passo 8: Enviar (Push)
Envie os arquivos para o GitHub.

```powershell
git push -u origin main
```

---

## 🚀 Resumo Rápido (Copie e Cole)

Se quiser fazer tudo de uma vez, rode estes comandos no terminal **dentro da pasta `reddit agents`**:

```powershell
# 1. Limpar clone acidental
if (Test-Path "Agentops") { Remove-Item -Recurse -Force "Agentops" }

# 2. Iniciar Git
git init

# 3. Adicionar arquivos
git add .

# 4. Commit
git commit -m "Initial commit"

# 5. Branch main
git branch -M main

# 6. Adicionar remoto
git remote add origin https://github.com/RafaelJoda/Agentops.git

# 7. Push
git push -u origin main
```
