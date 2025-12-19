# 🏢 AGENTE FREELANCER HQ - Painel de Controle (FreelancerOS)

Bem-vindo ao seu escritório virtual. Este repositório centraliza todas as operações do seu negócio digital, unificando ferramentas, agentes autônomos e utilitários de produtividade.

**Filosofia:** Alta Performance, Ética Profissional e Resultados Reais.

> 🚀 **NOVO**: Agente 24/7 Totalmente Autônomo! [Quick Start em 5 minutos →](QUICKSTART.md)

---

## 📜 Índice

1. [Diretrizes & Ética](#-diretrizes--ética)
2. [FreelancerOS (Utility Core)](#-freelanceros-the-ultimate-utility-core)
3. [Agentes Autônomos (Zero-Touch)](#-agente-freelancer-autônomo-zero-touch)
4. [Automação 24/7](#-novo-automação-247-e-auto-sustentabilidade)
5. [Ventures (Triple Threat)](#-ventures-the-freelancer-triple-threat-engine)
6. [Plano de Ação](#-plano-de-ação-diário)
7. [Sistema de Regras de IA](#-sistema-de-regras-para-ia)

---

## 🧠 Diretrizes & Ética

**Mentalidade de Responsabilidade:**
*   **Valor > Código:** Não vendemos linhas de código, vendemos soluções de negócios.
*   **Ética:** Respeitamos dados, privacidade e termos de uso das plataformas.
*   **Profissionalismo:** Comunicação clara e prazos cumpridos.

[Ler Código de Ética e Operações (docs/ETHICS_AND_OPERATIONS.md)](docs/ETHICS_AND_OPERATIONS.md)

---

## 🧰 FreelancerOS: The Ultimate Utility Core

**Localização:** `projects/FreelancerOS`
**Descrição:** Um "Super-App" com mais de 220 ferramentas utilitárias verificadas.

**Módulos Incluídos:**
*   📊 **Business & Math:** Calculadoras de ROI, Impostos, Juros.
*   📝 **Text & Data:** Manipulação de strings, formatação, extração de e-mails.
*   💾 **System & Files:** Gerenciamento de arquivos e backups.
*   🌐 **Media & Web:** Utilitários para URLs, imagens e vídeos.

**Quick Start:**
```bash
python projects/FreelancerOS/main.py
```

---

## 🤖 Agente Freelancer Autônomo (Zero-Touch)

**Localização:** `projects/auto_agent`
**Status:** OPERATIONAL | **Arquitetura:** Hunter-Brain-Hand

Este sistema trabalha em loop infinito, monitorando a web por trabalhos, analisando-os e criando propostas.

**Componentes:**
1.  **Hunter (`hunter.py`):** Monitora RSS feeds (WeWorkRemotely, etc).
2.  **Brain (`brain.py`):** Analisa descrições e decide a capacidade de execução.
3.  **Hand (`hand.py`):** Gera propostas persuasivas.

**Como Rodar (Loop Infinito):**
```bash
python projects/auto_agent/auto_main.py
```

*Configurações disponíveis em `projects/auto_agent/config.py`.*

---

## 🚀 Ventures: The Freelancer "Triple Threat" Engine

3 Negócios Escaláveis prontos para rodar.

### Venture 1: The Browser Agent
*   **Serviço:** Automação de tarefas web (preenchimento de formulários, data entry).
*   **Comando:** `python projects/browser_agent/navigator.py`

### Venture 2: The AI Crew
*   **Serviço:** Time de Marketing 24/7 com IA.
*   **Comando:** `python projects/ai_crew/crew_engine.py`

### Venture 3: The Script Vault (`projects/script_vault/`)
*   **PDF Master:** Merge e marca d'água em documentos legais.
*   **Image Optimizer:** Otimização em massa para e-commerce.
*   **Invoice Generator:** Geração de faturas em PDF.

---

## 📈 Plano de Ação Diário

1.  **Manhã (Prospecção):** Rode o **Lead Hunter** ou verifique os logs do **Zero-Touch Agent**.
2.  **Tarde (Vendas & Execução):** Envie propostas personalizadas e use os templates para fechar contratos.
3.  **Noite (Estudo & Melhoria):** Use o **GitHub Market Hunter** para expandir seu portfólio.

---

## 🤖 NOVO: Automação 24/7 e Auto-Sustentabilidade

O FreelancerOS agora suporta **operação totalmente autônoma e contínua** com recuperação automática de erros!

### 🚀 Implantação Rápida

**Opção 1: Docker (Recomendado)**
```bash
# Configure suas credenciais
cp .env.example .env
nano .env

# Implante com um comando
./system/scripts/deploy_docker.sh
```

**Opção 2: Systemd (Linux)**
```bash
# Implante como serviço do sistema
sudo ./system/scripts/deploy_systemd.sh
```

### 📊 Monitoramento

```bash
# Verifique a saúde do agente
python3 system/scripts/health_check.py

# Veja logs em tempo real
docker-compose logs -f  # Docker
sudo journalctl -u freelanceros-agent -f  # Systemd
```

### 💾 Backup Automático

```bash
# Execute backup manual
./system/scripts/backup.sh

# Configure cron para backups automáticos diários
0 2 * * * /path/to/FreelancerOS/system/scripts/backup.sh
```

### 🔑 Recursos de Auto-Sustentabilidade

✅ **Recuperação Automática de Erros** - O agente se recupera automaticamente de falhas  
✅ **Health Checks Periódicos** - Autodiagnóstico a cada 5 minutos  
✅ **Logging Abrangente** - Rastreamento completo de todas as operações  
✅ **Retry com Backoff Exponencial** - Tentativas inteligentes em caso de falha  
✅ **Reinício Automático** - Docker/Systemd reinicia o agente se ele parar  
✅ **Gestão de Recursos** - Monitoramento de memória e CPU  

📖 **[Guia Completo de Implantação](docs/DEPLOYMENT_GUIDE.md)**

---

## 🛡️ Sistema de Regras de IA

Este projeto adota uma política de **Tolerância Zero** para desorganização. Todas as IAs que interagirem com este repositório devem seguir estritamente o arquivo `AI_RULES.md`.

**Resumo das Regras:**
1.  🚫 **Proibido** criar arquivos soltos na raiz (root).
2.  📂 Todo novo arquivo deve estar numa pasta categorizada dentro de `projects/` ou `system/`.
3.  📝 Toda nova funcionalidade **DEVE** ser documentada neste README.

---

## 🏛️ Protocolo ARCHON v5.0 (Reasoning Engine)

O sistema evoluiu para uma entidade de raciocínio superior, operando sob o protocolo **ARCHON v5.0**.

### Pilares de Síntese
1.  **Investigação Filosófica Aplicada** (O Porquê)
2.  **SRE & Confiabilidade** (A Robustez)
3.  **Artesanato de Software** (A Qualidade)
4.  **Sistemas Adaptativos** (A Complexidade)
5.  **Ética Técnica** (A Responsabilidade)

### Ciclo Operacional
- **Avaliação:** Validação epistemológica da evidência.
- **Refinamento:** Redução de ambiguidade e aumento de precisão.
- **Ação de Valor:** Impacto > Risco > Utilidade.

**Protocolo de Saída:** KERNEL (Kickoff, Explicit Constraints, Reproducible Results, Narrow Scope, Evaluated Output, Logical Structure).
