import os
from google import genai
from google.api_core import exceptions
from google.genai.errors import ServerError
from dotenv import load_dotenv


class StoryImaginator(object):

    def __init__(self):
        self.gemini_api_key = ''
        self.instructions_path = 'gen-adventure/instructions.txt'
        self.client = genai.Client(api_key=self.gemini_api_key)

    def load_instructions(self):
        with open(self.instructions_path, "r", encoding="utf-8") as file:
            return file.read()
        

    def build_prompt(self, theme: str, instructions: str) -> str:
        return f"""
                Você é um criador de histórias interativas.

                Tema solicitado:
                {theme}

                Siga EXATAMENTE as instruções abaixo para gerar a resposta:

                {instructions}

                IMPORTANTE:

                - Retorne SOMENTE o conteúdo CSV
                - Não use markdown
                - Não use ```csv
                - Não explique nada antes
                - Não explique nada depois
                - A primeira linha deve ser:

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

    load_dotenv()

    imaginator = StoryImaginator()
    imaginator.gemini_api_key = os.getenv("GEMINI_API_KEY")

    try:
        imaginator.imagine("A detective investigating a murder scene", "gen-adventure/test2.csv")

    # except Exception as e:
    #     print("TIPO:", type(e))
    #     print("NOME:", type(e).__name__)
    #     print("MÓDULO:", type(e).__module__)
    #     print("MENSAGEM:", str(e))
    #     raise

    except ServerError:
        print("Error 503! This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.")