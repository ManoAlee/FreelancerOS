
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Auto-Agent: ENTERPRISE BRAIN (Scoring Engine)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import yaml

class EnterpriseBrain:
    def __init__(self, config_path="projects/auto_agent/config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.matrix = self.config['skills_matrix']
        self.threshold = self.config['filters']['min_confidence_score']
        self.blacklist = self.config['filters']['blacklist_words']

    def evaluate(self, job):
        """
        Calculates a 'Win Probability' score (0-100).
        """
        title = job['title'].lower()
        summary = job['summary'].lower()
        full_text = title + " " + summary
        
        # 1. Check Blacklist (Instant Kill)
        for bad_word in self.blacklist:
            if bad_word in full_text:
                return {"decision": "REJECT", "score": 0, "reason": f"Blacklisted: {bad_word}"}

        # 2. Calculate Score
        score = 0
        matches = []
        
        for skill, weight in self.matrix.items():
            if skill in title:
                score += weight * 2 # Title matches depend double
                matches.append(f"{skill}(Title)")
            elif skill in summary:
                score += weight
                matches.append(skill)
        
        # Normalize (Cap at 99 for realism)
        final_score = min(score + 50, 99) # Base score 50 just for showing up?? No, let's say base match.
        
        # Actually, let's map raw points to a 0-100 scale better.
        # Say 20 points = 80%.
        # Baseline = 40.
        final_score = 40 + score
        final_score = min(final_score, 99)

        # 3. Decision
        if final_score >= self.threshold:
            return {
                "decision": "APPLY",
                "score": final_score,
                "reason": f"Matched: {', '.join(matches)}",
                "plan": f"Use {matches[0] if matches else 'General'} Tools"
            }
        else:
            return {
                "decision": "IGNORE",
                "score": final_score,
                "reason": "Score below threshold"
            }
