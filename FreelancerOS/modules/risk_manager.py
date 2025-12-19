import time
import random
import logging

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🛡️ MÓDULO: GESTÃO DE RISCO & HUMANIZAÇÃO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Objetivo: Impedir que a conta seja banida.
# Simula cansaço, pausas para café e horários de sono.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class RiskManager:
    def __init__(self):
        self.actions_count = 0
        self.max_actions_per_hour = 20

    def check_safety(self):
        """Verifica se é seguro continuar operando."""
        if self.actions_count > self.max_actions_per_hour:
            print("   ⚠️ Limite de ações por hora atingido. Pausando...")
            self.take_long_break()
            self.actions_count = 0
        return True

    def human_delay(self):
        """Pausa curta aleatória entre cliques."""
        delay = random.uniform(2, 8)
        time.sleep(delay)

    def take_long_break(self):
        """Pausa longa (café/almoço)."""
        minutes = random.randint(10, 30)
        print(f"   ☕ Tomando um café... (Pausa de {minutes} min)")
        time.sleep(minutes * 60)

    def register_action(self):
        self.actions_count += 1
