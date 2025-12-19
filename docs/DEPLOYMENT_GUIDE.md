# 🚀 GUIA DE IMPLANTAÇÃO - AGENTE AUTÔNOMO 24/7

Este guia explica como implantar o FreelancerOS Agent para operação contínua e autossustentável.

---

## 📋 Pré-requisitos

### Sistema Operacional
- Linux (Ubuntu 20.04+, Debian 10+, CentOS 8+)
- macOS 10.15+
- Windows 10+ (com WSL2)

### Software Necessário
- Python 3.8 ou superior
- Docker (opcional, recomendado)
- Git

---

## 🐳 Opção 1: Implantação com Docker (Recomendado)

Docker facilita a implantação e garante consistência em qualquer ambiente.

### Passo 1: Instalar Docker

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Passo 2: Configurar Ambiente

```bash
# Clone o repositório (se ainda não o fez)
git clone https://github.com/ManoAlee/FreelancerOS.git
cd FreelancerOS

# Copie e edite o arquivo de configuração
cp .env.example .env
nano .env  # ou use seu editor preferido
```

**Configure as seguintes variáveis importantes:**

```bash
# Suas credenciais de email
MY_EMAIL=seu_email@gmail.com
MY_PASSWORD=sua_senha_de_app_aqui

# Nicho alvo
TARGET_NICHE=advogados em são paulo

# Comportamento
MODE=AGGRESSIVE
AUTO_SEND_EMAIL=True
```

### Passo 3: Implantar

```bash
# Execute o script de implantação
./system/scripts/deploy_docker.sh
```

### Passo 4: Gerenciar o Agente

```bash
# Ver logs em tempo real
docker-compose logs -f

# Parar o agente
docker-compose down

# Reiniciar o agente
docker-compose restart

# Ver status
docker-compose ps
```

---

## 🖥️ Opção 2: Implantação com Systemd (Linux Nativo)

Para servidores Linux sem Docker, use systemd para gerenciar o serviço.

### Passo 1: Preparar o Ambiente

```bash
# Clone o repositório
git clone https://github.com/ManoAlee/FreelancerOS.git
cd FreelancerOS

# Configurar ambiente
cp .env.example .env
nano .env  # edite suas credenciais
```

### Passo 2: Implantar como Serviço

```bash
# Execute com sudo
sudo ./system/scripts/deploy_systemd.sh
```

Este script irá:
- Instalar dependências Python
- Criar o serviço systemd
- Habilitar início automático
- Iniciar o serviço

### Passo 3: Gerenciar o Serviço

```bash
# Ver logs em tempo real
sudo journalctl -u freelanceros-agent -f

# Parar
sudo systemctl stop freelanceros-agent

# Iniciar
sudo systemctl start freelanceros-agent

# Reiniciar
sudo systemctl restart freelanceros-agent

# Ver status
sudo systemctl status freelanceros-agent

# Desabilitar início automático
sudo systemctl disable freelanceros-agent
```

---

## ☁️ Opção 3: Implantação na Nuvem

### AWS EC2

```bash
# 1. Crie uma instância EC2 (Ubuntu 22.04)
# 2. Conecte via SSH
ssh -i sua-chave.pem ubuntu@seu-ip

# 3. Instale Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 4. Clone e configure
git clone https://github.com/ManoAlee/FreelancerOS.git
cd FreelancerOS
cp .env.example .env
nano .env

# 5. Implante
./system/scripts/deploy_docker.sh
```

### Google Cloud Platform (GCP)

```bash
# 1. Crie uma VM Compute Engine
# 2. Mesmo processo da AWS EC2
```

### DigitalOcean

```bash
# 1. Crie um Droplet (Ubuntu)
# 2. Mesmo processo da AWS EC2
```

### Heroku

```bash
# 1. Instale Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# 2. Login
heroku login

# 3. Crie app
heroku create seu-app-freelanceros

# 4. Configure variáveis de ambiente
heroku config:set MY_EMAIL=seu_email@gmail.com
heroku config:set MY_PASSWORD=sua_senha

# 5. Deploy
git push heroku main
```

---

## 🔒 Segurança

### Proteção de Credenciais

1. **Nunca commite o arquivo .env**
   ```bash
   # Já está no .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use senhas de aplicativo** (não sua senha real)
   - Gmail: https://myaccount.google.com/apppasswords
   - Gere uma senha específica para o agente

3. **Restrinja acesso SSH** (se em servidor)
   ```bash
   # Edite sshd_config
   sudo nano /etc/ssh/sshd_config
   # PasswordAuthentication no
   # PubkeyAuthentication yes
   ```

---

## 📊 Monitoramento

### Verificar Saúde do Agente

```bash
# Docker
docker-compose ps
docker-compose logs --tail=50

# Systemd
systemctl status freelanceros-agent
journalctl -u freelanceros-agent --since "10 minutes ago"
```

### Métricas no Banco de Dados

```bash
# Conecte ao container
docker-compose exec freelancer-agent python3

# No Python:
from system.data_pipeline.recorder import JobRecorder
recorder = JobRecorder()
print(recorder.get_stats())
```

---

## 🔧 Troubleshooting

### Problema: O agente não inicia

**Solução:**
```bash
# Verifique logs
docker-compose logs

# Verifique configuração
cat .env

# Reconstrua a imagem
docker-compose build --no-cache
docker-compose up -d
```

### Problema: Erros de autenticação de email

**Solução:**
1. Verifique se está usando senha de aplicativo
2. Habilite "Acesso de apps menos seguros" (Gmail)
3. Teste credenciais manualmente

### Problema: O agente para após algum tempo

**Solução:**
```bash
# Verifique memória e recursos
docker stats

# Aumente recursos do container (docker-compose.yml)
# Ou use systemd que gerencia melhor
```

### Problema: Não encontra jobs

**Solução:**
1. Verifique se os RSS feeds estão acessíveis
2. Ajuste `TARGET_NICHE` no .env
3. Reduza `MIN_CONFIDENCE_SCORE`

---

## 🔄 Atualização

### Atualizar o Agente

```bash
# Para a execução
docker-compose down  # ou sudo systemctl stop freelanceros-agent

# Atualize o código
git pull origin main

# Reconstrua e reinicie
docker-compose build
docker-compose up -d

# Ou para systemd
sudo systemctl restart freelanceros-agent
```

---

## 📞 Suporte

- **Issues:** https://github.com/ManoAlee/FreelancerOS/issues
- **Documentação:** README.md
- **Ética:** docs/ETHICS_AND_OPERATIONS.md

---

## ✅ Checklist de Implantação

- [ ] Docker instalado (ou Python 3.8+)
- [ ] Repositório clonado
- [ ] Arquivo .env configurado com credenciais
- [ ] Script de implantação executado
- [ ] Agente rodando (verificar logs)
- [ ] Health check passando
- [ ] Monitoramento configurado
- [ ] Backup de dados configurado

---

**🎉 Parabéns! Seu agente está operacional 24/7!**
