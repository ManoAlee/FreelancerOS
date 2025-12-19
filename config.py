# ⚙️ CENTRAL DE COMANDO (Configure uma vez, esqueça depois)

CONFIG = {
    # 🎯 QUEM VAMOS ATACAR?
    "TARGET_NICHE": "advogados em são paulo",
    "MAX_LEADS_PER_DAY": 50,
    
    # 🤖 COMPORTAMENTO DO ROBÔ
    "MODE": "AGGRESSIVE", # 'SAFE' (Lento/Seguro) ou 'AGGRESSIVE' (Rápido)
    "WORK_HOURS": [9, 18], # Trabalha apenas das 09h às 18h
    
    # 📧 AUTOMAÇÃO DE VENDAS
    "AUTO_SEND_EMAIL": True, # Se False, apenas salva o rascunho
    "MY_EMAIL": "seu_email@gmail.com",
    "MY_PASSWORD": "sua_senha_de_app",
    
    # 🕷️ FONTES DE DADOS
    "SOURCES": [
        "https://www.google.com/search?q={niche}",
        "https://www.instagram.com/explore/tags/{niche}/"
    ],
    
    # 📝 MODELO DE PROPOSTA (O Robô preenche sozinho)
    "EMAIL_SUBJECT": "Parceria para {empresa}",
    "EMAIL_BODY": """
    Olá, vi que a {empresa} tem um grande potencial.
    Sou um agente autônomo especializado em web.
    Criei um pré-projeto para vocês. Podemos conversar?
    """
}
