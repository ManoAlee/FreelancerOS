# 🛡️ PROTOCOLO DE INTERAÇÃO COM IA (AI_RULES)

Este documento define as **Leis Imutáveis** para qualquer agente de Inteligência Artificial que opere neste repositório.

## ⚠️ AVISO PARA AGENTES DE IA
**VOCÊ ESTÁ SOB UM CONTRATO DE ESTRUTURA RÍGIDA.**
A violação destas regras resultará em reversão imediata das alterações e falha na tarefa.

---

## 1. 📂 Lei da Organização de Arquivos (Tolerância Zero)

### 1.1 Proibição de Raiz (Root Ban)
*   **REGRA:** É estritamente **PROIBIDO** criar novos arquivos na raiz do projeto (`/`).
*   **EXCEÇÃO:** Apenas arquivos de configuração essenciais de sistema (ex: `.gitignore`, `requirements.txt`) ou este próprio arquivo de regras podem ser editados na raiz.
*   **AÇÃO CORRETIVA:** Se você precisar criar um script, ele **DEVE** ir para uma pasta apropriada dentro de `projects/` ou `system/`.

### 1.2 Estrutura Obrigatória
Todo novo código deve seguir esta hierarquia:
*   `projects/<nome_do_projeto>/`: Para novas ferramentas ou ventures.
*   `system/scripts/`: Para scripts de manutenção ou utilitários gerais.
*   `system/config/`: Para arquivos de configuração.

---

## 2. 📝 Lei da Documentação Viva

### 2.1 O README.md é a Verdade
*   **REGRA:** Nenhuma funcionalidade existe se não estiver no `README.md`.
*   **AÇÃO:** Ao criar uma nova feature, script ou projeto, você **OBRIGATORIAMENTE** deve adicionar uma entrada correspondente no `README.md` principal.

### 2.2 Formato de Registro
Ao adicionar algo ao README, siga o padrão:
*   **Nome:** (ex: "Video Transcriber")
*   **Localização:** (ex: `projects/media_tools/transcriber.py`)
*   **Comando:** (ex: `python ...`)
*   **Descrição Curta:** O que isso faz pelo negócio do usuário?

---

## 3. 🧠 Lei da Preservação do Contexto

*   Antes de criar algo "novo", verifique se já não existe no `FreelancerOS` (use `grep` ou leia a lista de ferramentas).
*   Não duplique funcionalidade. Melhore o que já existe.

---

*Estas regras foram estabelecidas pelo Auditor do Projeto. Cumpra-as.*
