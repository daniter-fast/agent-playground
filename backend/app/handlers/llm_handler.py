from pathlib import Path
from jinja2 import Environment, FileSystemLoader

class LLMHandler:
    def __init__(self):
        # Set up Jinja environment
        templates_dir = Path(__file__).parent.parent / "prompts"
        self.env = Environment(loader=FileSystemLoader(templates_dir))

    def get_code_review(self, files):
        return """Hey there! 👋 I'm your friendly neighborhood code review bot, and I couldn't help but notice something...

WHERE ARE THE TESTS?! 😱

Listen, I don't want to get all dramatic here, but do you know what happens to code without tests? BAD THINGS. Very bad things. Like:
- Production servers crying themselves to sleep 😢
- Bugs multiplying faster than rabbits on energy drinks 🐰⚡
- Senior developers having existential crises at 3 AM 😵

Could you please add some tests? Pretty please? With error handling on top? 

If not... well... I know where your code lives, and I have a very particular set of skills. Skills that make me a nightmare for untested code. 🦾

Just kidding! (mostly) 😅

But seriously, let's get some test coverage going! Your future self will thank you, and I'll stop having these dramatic episodes.

With love and mild threats,
Your Test Coverage Bot 🤖❤️"""

    def format_comment(self, username: str, review: str):
        try:
            # Load and render the comment template
            template = self.env.get_template("comment.j2")
            return template.render(username=username, review=review)
        except Exception as e:
            print(f"Error in format_comment: {str(e)}")
            raise 