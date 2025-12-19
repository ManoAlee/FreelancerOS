import time
import random
import logging
import os
from openai import OpenAI

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🧠 MÓDULO: GERADOR DE PROPOSTAS (BID GENERATOR)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Objetivo: Criar propostas que parecem escritas por humanos,
# focadas na dor do cliente e não em "eu sou bom".
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ProposalEngine:
    def __init__(self, persona):
        self.persona = persona
        self.logger = logging.getLogger('ProposalEngine')
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def generate_bid(self, project_title, project_description, client_name="Client"):
        """
        Gera uma proposta personalizada baseada no projeto.
        Usa OpenAI se disponível, senão usa templates.
        """
        print(f"   ✍️ Escrevendo proposta para: '{project_title}'...")
        
        # Simulação de "Pensamento" da IA
        time.sleep(random.uniform(1, 3))
        
        if self.client:
            try:
                return self._generate_ai_bid(project_title, project_description)
            except Exception as e:
                self.logger.error(f"Erro na OpenAI: {e}. Usando template.")
        
        if self.persona == "SENIOR_DEV":
            return self._template_dev(client_name, project_title)
        elif self.persona == "COPYWRITER":
            return self._template_copy(client_name, project_title)
        else:
            return self._template_generic(client_name)

    def _generate_ai_bid(self, title, description):
        prompt = f"""
        Você é um freelancer experiente ({self.persona}).
        Escreva uma proposta curta, direta e profissional para este projeto:
        
        Título: {title}
        Descrição: {description}
        
        Regras:
        1. Não use saudações genéricas como "Dear Hiring Manager".
        2. Foque em como resolver o problema.
        3. Máximo de 100 palavras.
        4. Termine com uma chamada para ação (Call to Action).
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        return response.choices[0].message.content

    def _template_dev(self, name, title):
        return f"""
        Hi {name},
        
        I read your project "{title}" and I can solve this quickly.
        
        I am a Senior Python Developer specialized in automation. 
        I have a script ready that does exactly what you need (Scraping/Automation).
        
        I can deliver this in 24 hours.
        
        Let's chat?
        """

    def _template_copy(self, name, title):
        return f"""
        Hello {name},
        
        Need high-converting text for "{title}"? I'm your guy.
        I write copy that sells, not just fills space.
        
        Check my portfolio attached.
        """

    def _template_generic(self, name):
        return f"Hi {name}, I can help with this project. Please check my reviews."
