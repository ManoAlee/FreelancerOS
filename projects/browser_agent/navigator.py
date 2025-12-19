from playwright.sync_api import sync_playwright
import time
import random

class SmartNavigator:
    """
    A Freelancer-Ready Browser Agent.
    Simplifies complex Playwright actions into human-readable commands.
    """
    def __init__(self, headless=False):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None

    def start(self):
        """Initializes the browser session."""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.page = self.browser.new_page()
        print("🤖 Browser Agent Activated.")

    def stop(self):
        """Closes the browser session."""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("💤 Agent Sleeping.")

    def go_to(self, url):
        """Navigates to a URL with human-like delays."""
        print(f"🔗 Navigating to: {url}")
        self.page.goto(url)
        self.human_delay()

    def click_text(self, text):
        """Clicks an element containing specific text."""
        print(f"🖱️ Clicking: '{text}'")
        try:
            self.page.get_by_text(text, exact=False).first.click()
            self.human_delay()
        except Exception as e:
            print(f"❌ Failed to click '{text}': {e}")

    def fill_form(self, data):
        """
        Fills a form based on a dictionary {Label: Value}.
        Uses intelligent label matching.
        """
        print("📝 Filling Form...")
        for label, value in data.items():
            try:
                # Try to find input by placeholder or label
                self.page.get_by_label(label).fill(value)
                print(f"   ✅ Filled '{label}'")
            except:
                try:
                    self.page.get_by_placeholder(label).fill(value)
                    print(f"   ✅ Filled '{label}' (via placeholder)")
                except Exception as e:
                    print(f"   ❌ Could not fill '{label}'")
            self.human_delay()

    def human_delay(self):
        """Random delay to simulate human focus."""
        time.sleep(random.uniform(0.5, 2.0))

    def screenshot(self, filename="evidence.png"):
        """Takes a screenshot proof."""
        self.page.screenshot(path=filename)
        print(f"📸 Screenshot saved: {filename}")

# --- DEMO USAGE ---
if __name__ == "__main__":
    # Example: Automating a search and form fill
    agent = SmartNavigator(headless=False)
    try:
        agent.start()
        agent.go_to("https://saucedemo.com") # Demo testing site
        agent.fill_form({
            "Username": "standard_user",
            "Password": "secret_sauce"
        })
        # Note: Selectors might need tweaking for specific sites, 
        # but this 'fill_form' tries its best with generic labels.
        input("Press Enter to close agent...")
    finally:
        agent.stop()
