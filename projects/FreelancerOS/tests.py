
import unittest
import sys
import os

# Adapt path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from freelanceros.modules import business_math, text_data, system_files, media_web

class TestFreelancerOS(unittest.TestCase):
    def test_tool_count(self):
        """Verify we have enough tools."""
        modules = [business_math, text_data, system_files, media_web]
        total = 0
        for mod in modules:
            funcs = [f for f in dir(mod) if not f.startswith('_')]
            total += len(funcs)
        
        print(f"\n🔥 Verified Function Count: {total}")
        self.assertTrue(total >= 200, f"Expected 200+, found {total}")

    def test_business_logic(self):
        self.assertEqual(business_math.calc_profit_margin(100, 50), 50.0)
    
    def test_text_logic(self):
        self.assertEqual(text_data.slugify("Hello World"), "hello-world")

if __name__ == '__main__':
    unittest.main()
