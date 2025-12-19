# 🚀 QUICK START - FreelancerOS 24/7 Agent

Guia rápido para colocar seu agente autônomo em operação em menos de 5 minutos!

---

## ⚡ Início Rápido com Docker

### 1. Clone e Configure (2 minutos)

```bash
# Clone o repositório
git clone https://github.com/ManoAlee/FreelancerOS.git
cd FreelancerOS

# Configure credenciais
cp .env.example .env
nano .env  # ou seu editor preferido
```

**Configurações Mínimas Necessárias:**
```bash
MY_EMAIL=seu_email@gmail.com
MY_PASSWORD=sua_senha_de_app
TARGET_NICHE=seu_nicho_aqui
```

### 2. Implante (1 minuto)

```bash
# Execute o script de deployment
chmod +x system/scripts/deploy_docker.sh
./system/scripts/deploy_docker.sh
```

### 3. Monitore

```bash
# Ver logs em tempo real
docker-compose logs -f

# Ver status de saúde
python3 system/scripts/health_check.py
```

✅ **Pronto!** Seu agente está rodando 24/7 e se recuperando automaticamente de erros.

---

## 📊 Comandos Úteis

### Gerenciamento Docker

```bash
# Ver status
docker-compose ps

# Parar
docker-compose down

# Reiniciar
docker-compose restart

# Ver logs (últimas 100 linhas)
docker-compose logs --tail=100
```

### Monitoramento

```bash
# Health check completo
python3 system/scripts/health_check.py

# Ver estatísticas do banco de dados
python3 -c "from system.data_pipeline.recorder import JobRecorder; print(JobRecorder().get_stats())"
```

### Backup

```bash
# Backup manual
./system/scripts/backup.sh

# Configurar backups automáticos
./system/scripts/setup_backup_cron.sh
```

---

## 🔧 Troubleshooting Rápido

### Problema: Container não inicia

```bash
# Ver erros
docker-compose logs

# Reconstruir imagem
docker-compose build --no-cache
docker-compose up -d
```

### Problema: Erros de autenticação email

1. Use **senha de aplicativo**, não sua senha normal
2. Gmail: https://myaccount.google.com/apppasswords
3. Habilite acesso a apps menos seguros (se necessário)

### Problema: Não encontra jobs

1. Verifique RSS feeds no .env
2. Ajuste `MIN_CONFIDENCE_SCORE` (tente 50 para testes)
3. Mude `TARGET_NICHE` para algo mais amplo

---

## 🌐 Opção 2: Deployment em VPS/Servidor

### Requerimentos
- Ubuntu 20.04+ / Debian 10+ / CentOS 8+
- Python 3.8+
- Acesso root/sudo

### Passos

```bash
# 1. Clone
git clone https://github.com/ManoAlee/FreelancerOS.git
cd FreelancerOS

# 2. Configure
cp .env.example .env
nano .env

# 3. Implante como serviço systemd
sudo ./system/scripts/deploy_systemd.sh

# 4. Verifique status
sudo systemctl status freelanceros-agent
```

---

## 📱 Notificações

Para receber alertas por email sobre o status do agente:

```bash
# No .env, configure:
NOTIFICATION_EMAIL_ENABLED=true
NOTIFICATION_EMAIL=seu_email@gmail.com
```

Você receberá notificações sobre:
- ✅ Início do agente
- ⚠️ Erros críticos
- 🔄 Reinicializações
- 📊 Resumo diário de atividades
- 🎯 Marcos (100, 200, 300 jobs processados)

---

## 🎯 Próximos Passos

Após ter o agente rodando:

1. **Monitore os logs** nas primeiras horas
2. **Ajuste configurações** baseado nos resultados
3. **Configure backups automáticos**
4. **Personalize propostas** em `system/config/config.py`
5. **Expanda fontes** adicionando mais RSS feeds

---

## 📚 Documentação Completa

- **Guia de Implantação Detalhado**: [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)
- **README Principal**: [README.md](README.md)
- **Código de Ética**: [docs/ETHICS_AND_OPERATIONS.md](docs/ETHICS_AND_OPERATIONS.md)

---

## 🆘 Suporte

- **Issues**: https://github.com/ManoAlee/FreelancerOS/issues
- **Documentação**: https://github.com/ManoAlee/FreelancerOS

---

**🎉 Bem-vindo ao FreelancerOS - Seu negócio agora opera 24/7!**
