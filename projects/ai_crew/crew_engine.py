import time

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🤖 AI CREW ENGINE (Template)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Build your own "Agency" of agents.
# Requires: OpenAI API Key (or change 'llm_call' to use another provider)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Agent:
    def __init__(self, role, goal, backstory):
        self.role = role
        self.goal = goal
        self.backstory = backstory

    def execute(self, task_description):
        print(f"\n👤 **Agent {self.role}** is working...")
        print(f"   🎯 Goal: {self.goal}")
        print(f"   📜 Task: {task_description}")
        
        # MOCK LLM CALL (Replace with actual OpenAI/Anthropic call)
        # return call_openai(system=self.backstory, user=task_description)
        
        time.sleep(1.5) # Thinking...
        result = f"[Output from {self.role}]: Based on my expertise in {self.role}, here is the result for '{task_description}'..."
        print("   ✅ Task Completed.")
        return result

class Task:
    def __init__(self, description, agent):
        self.description = description
        self.agent = agent

class Crew:
    def __init__(self, agents, tasks):
        self.agents = agents
        self.tasks = tasks

    def kick_off(self):
        print("🚀 Crew Starting Operations...")
        results = []
        for task in self.tasks:
            result = task.agent.execute(task.description)
            results.append(result)
        
        print("\n🏁 Mission Accomplished.")
        return results

# --- DEMO CONFIGURATION ---
if __name__ == "__main__":
    # Define Agents
    researcher = Agent(
        role="Senior Researcher",
        goal="Uncover groundbreaking technology trends",
        backstory="You are a veteran tech journalist who digs deep."
    )
    
    writer = Agent(
        role="Content Strategist",
        goal="Write viral blog posts",
        backstory="You turn dry data into compelling narratives."
    )

    # Define Tasks
    task1 = Task(
        description="Research the top 3 AI trends in 2025.",
        agent=researcher
    )
    
    task2 = Task(
        description="Write a 2-paragraph summary based on the research.",
        agent=writer
    )

    # Launch Crew
    my_crew = Crew(agents=[researcher, writer], tasks=[task1, task2])
    my_crew.kick_off()
