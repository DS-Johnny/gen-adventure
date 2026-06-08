import os
from google import genai
import json
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

                * If the requested theme is written in English, the entire story must be written in English.
                * If the requested theme is written in Portuguese, the entire story must be written in Portuguese.
                * All narrative text, dialogues, descriptions, endings, and choices must consistently use the same language as the requested theme.
                * Never mix languages unless the requested theme explicitly requires it.

                Follow EXACTLY the instructions below to generate the response:

                {instructions}

                CRITICAL REQUIREMENTS:

                * Return ONLY a valid JSON object.
                * Do not use Markdown.
                * Do not use code blocks.
                * Do not use ```json.
                * Do not provide any explanation before the JSON.
                * Do not provide any explanation after the JSON.
                * Do not add comments.
                * Do not add notes.
                * Do not add warnings.
                * Do not add formatting instructions.
                * The response must be directly parsable by json.loads().
                * The response must start with an opening curly brace: {{
                * The response must end with a closing curly brace: }}

                FINAL VALIDATION:

                Before generating the response, internally verify that:

                * The output is valid JSON.
                * The root object contains the "pages" property.
                * Every page contains:

                * id
                * text
                * options
                * Every option contains:

                * text
                * target
                * All target IDs exist.
                * All pages are reachable from page 1.
                * The story follows all instructions provided in {instructions}.
                * The JSON is compatible with Python json.loads().

                Return ONLY the JSON object.

                """

    def generate_story_json(self, theme: str) -> str:

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
    

    def save_json(self, content: str, filename: str):

        data = json.loads(content)

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

    def imagine(self, theme, filename):
        json_content = self.generate_story_json(theme)

        self.save_json(json_content, filename)

if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    imaginator = StoryImaginator()
    imaginator.gemini_api_key = os.getenv("GEMINI_API_KEY")

    imaginator.imagine("Uma garota no baile de formatura", "gen_adventure/formatura.json")

