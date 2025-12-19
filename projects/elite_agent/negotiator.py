
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Elite Agent: NEGOTIATOR (Interaction Layer)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Persona:
    def __init__(self, name, tone, capability_focus):
        self.name = name
        self.tone = tone # e.g., "Executive", "Technical", "Creative"
        self.focus = capability_focus

# The Library of Faces
PERSONAS = {
    "developer": Persona("Senior Python Engineer", "Technical & Precise", "backend optimization"),
    "designer": Persona("Creative Visual Lead", "Enthusiastic & Visionary", "user experience"),
    "analyst": Persona("Data Scientist", "Analytical & Objective", "insight generation")
}

class Negotiator:
    def __init__(self):
        self.personas = PERSONAS

    def select_persona(self, job_title):
        """Automatically selects the best 'Face' for the job."""
        title = job_title.lower()
        if "design" in title or "ui" in title or "logo" in title:
            return self.personas["designer"]
        elif "data" in title or "scrape" in title or "analysis" in title:
            return self.personas["analyst"]
        else:
            return self.personas["developer"]

    def craft_bid(self, job, persona):
        """
        Generates a tailored proposal using the selected Persona strategy.
        Note: This does NOT print. It returns string data for the system.
        """
        # Dynamic Hook (Referencing the job)
        hook = f"Regarding your need for {job['title']}..."
        
        # Persona Injection
        if persona.tone == "Technical & Precise":
            body = f"I have analyzed your requirements. My stack focuses on {persona.focus}. I propose a modular architecture to solve this efficiently."
            closer = "Ready to deploy."
        elif persona.tone == "Enthusiastic & Visionary":
            body = f"I love this concept! My focus on {persona.focus} will bring this to life with premium aesthetics. I can already visualize the result."
            closer = "Let's create something amazing."
        else:
            body = f"I have reviewed the metrics. Applying my {persona.focus} techniques will ensure maximum accuracy."
            closer = "Awaiting access to data."

        # The "Offer" (Mocked logic)
        offer = f"Estimated Delivery: 24h"

        return f"""
        [INTERNAL ID: {job['id']}]
        [PERSONA: {persona.name}]
        
        Hi,
        
        {hook}
        
        {body}
        
        {offer}
        
        {closer}
        """
