# 🤖 AGENTE FREELANCER AUTÔNOMO (ZERO TOUCH)

Este projeto foi refatorado para funcionar sozinho. Você não precisa mais escolher opções em um menu.
Você configura o objetivo, dá o "Play" e vai viver sua vida.

## ⚙️ Como Configurar
Edite o arquivo `config.py`:
```python
CONFIG = {
    "TARGET_NICHE": "dentistas em curitiba",
    "AUTO_SEND_EMAIL": True, # Cuidado! Isso envia emails reais.
    ...
}
```

## 🚀 Como Iniciar
Abra o terminal e rode:
```powershell
python autopilot.py
```

## 🧠 O que ele faz sozinho?
1.  **Acorda** às 09:00 da manhã.
2.  **Busca** sites no Google baseados no seu nicho.
3.  **Entra** em cada site e procura emails/telefones.
4.  **Envia** uma proposta comercial personalizada automaticamente.
5.  **Dorme** aleatoriamente para parecer humano.
6.  **Para** às 18:00.

## 📊 Onde vejo os resultados?
Abra o arquivo `agent_activity.log` para ver o diário de bordo do seu robô.

---
*"Enquanto você dorme, o Agente trabalha."*
