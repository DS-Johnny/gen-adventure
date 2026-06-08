import os
from google import genai
# from google.api_core import exceptions
# from google.genai.errors import ServerError, ClientError


class StoryImaginator(object):

    def __init__(self):
        self.gemini_api_key = ''
        self.instructions_path = 'gen_adventure/instructions.txt'
        self.client = genai.Client(api_key=self.gemini_api_key)

    def load_instructions(self):
        with open(self.instructions_path, "r", encoding="utf-8") as file:
            return file.read()
        

    def build_prompt(self, theme: str, instructions: str) -> str:
        return f"""
                You are an interactive story creator.

                Requested theme:
                {theme}

                LANGUAGE RULE:

                If the requested theme is written in English, the entire story must be written in English.
                If the requested theme is written in Portuguese, the entire story must be written in Portuguese.
                All narrative text, dialogues, descriptions, endings, and choices must consistently use the same language as the requested theme.

                Follow EXACTLY the instructions below to generate the response:

                {instructions}

                IMPORTANT:

                Return ONLY the CSV content.
                Do not use Markdown.
                Do not use ```csv.
                Do not provide any explanation before the CSV.
                Do not provide any explanation after the CSV.
                The first line must be exactly:

                id,text,options
                """

    def generate_story_csv(self, theme: str) -> str:

        instructions = self.load_instructions()

        prompt = self.build_prompt(
            theme=theme,
            instructions=instructions
        )

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text.strip()
    
    def save_csv(self, content: str, filename: str):

        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)

    def imagine(self, theme, filename):
        csv_content = self.generate_story_csv(theme)

        self.save_csv(csv_content, filename)

if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    imaginator = StoryImaginator()
    imaginator.gemini_api_key = os.getenv("GEMINI_API_KEY")

    imaginator.imagine("A detective investigating a murder scene", "gen_adventure/test2.csv")

