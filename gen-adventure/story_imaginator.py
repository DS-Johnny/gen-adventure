import os
from pathlib import Path
from google import genai


# -----------------------------------------
# Config
# -----------------------------------------



client = genai.Client(
    api_key="GEMINI_API_KEY"
)

INSTRUCTIONS_FILE = Path("instructions.txt")


# -----------------------------------------
# Lê arquivo txt com instruções
# -----------------------------------------

def load_instructions() -> str:
    with open(INSTRUCTIONS_FILE, "r", encoding="utf-8") as file:
        return file.read()


# -----------------------------------------
# Monta prompt final
# -----------------------------------------

def build_prompt(theme: str, instructions: str) -> str:
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

id,texto,opções
"""


# -----------------------------------------
# Gera CSV usando Gemini
# -----------------------------------------

def generate_story_csv(theme: str) -> str:

    instructions = load_instructions()

    prompt = build_prompt(
        theme=theme,
        instructions=instructions
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()


# -----------------------------------------
# Salva CSV
# -----------------------------------------

def save_csv(content: str, filename: str):

    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)


# -----------------------------------------
# Execução
# -----------------------------------------

if __name__ == "__main__":

    theme = input("Digite o tema da história: ")

    csv_content = generate_story_csv(theme)

    output_file = "historia_interativa.csv"

    save_csv(
        csv_content,
        output_file
    )

    print(f"\nArquivo salvo com sucesso em: {output_file}")