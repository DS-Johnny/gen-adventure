"""
Story generation module.

This module provides the StoryImaginator class, which uses the
Google Gemini API to create interactive branching stories and
export them as JSON files compatible with Gen-Adventure.
"""

from google import genai
import json
from google.genai.errors import ServerError
import requests
from time import sleep


class StoryImaginator(object):
    """
    Generate interactive story files using the Gemini API.

    This class is responsible for:

    - Loading generation instructions.
    - Building prompts for the language model.
    - Requesting story generation from Gemini.
    - Validating and saving the generated JSON output.
    """

    def __init__(self) -> None:
        """
        Initialize the Gemini client and configure default paths.

        The instructions file contains the rules and structure used
        to generate interactive stories.
        """

        self.gemini_api_key = ''

        # Path to the prompt instructions file.
        self.instructions_path = 'gen_adventure/instructions.txt'

        # Gemini API client.
        self.client = genai.Client(api_key=self.gemini_api_key)

    def load_instructions(self) -> str:
        """
        Download the story generation instructions from the project's
        GitHub repository.

        Returns
        -------
        str
            Content of the instructions file.

        Raises
        ------
        requests.exceptions.RequestException
            Raised if the instructions file cannot be retrieved.
        """

        # Raw GitHub URL containing the story generation rules.
        url = (
            "https://raw.githubusercontent.com/"
            "DS-Johnny/gen-adventure/main/"
            "gen_adventure/instructions.txt"
        )

        # Download the instructions file.
        response = requests.get(url, timeout=10)

        # Raise an exception for HTTP errors.
        response.raise_for_status()

        return response.text


    def build_prompt(self, theme: str, instructions: str) -> str:
        """
        Build the prompt sent to Gemini.

        The generated prompt includes:

        - The requested story theme.
        - Language consistency rules.
        - Story generation instructions.
        - JSON output requirements.
        - Validation constraints to ensure a valid story structure.

        Parameters
        ----------
        theme : str
            Theme provided by the user.
        instructions : str
            Story generation instructions loaded from file.

        Returns
        -------
        str
            Fully formatted prompt ready to be sent to Gemini.
        """

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
        """
        Generate a story in JSON format using Gemini.

        Parameters
        ----------
        theme : str
            Theme used as the basis for story generation.

        Returns
        -------
        str
            Raw JSON string returned by the model.
        """

        # Load generation rules.
        instructions = self.load_instructions()
        
        # Build the final prompt.
        prompt = self.build_prompt(
            theme=theme,
            instructions=instructions
        )

        # Request content generation from Gemini.
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text.strip()
    

    def save_json(self, content: str, filename: str) -> None:
        """
        Validate and save generated JSON content to a file.

        Parameters
        ----------
        content : str
            JSON string generated by Gemini.
        filename : str
            Output file path.
        """

        # Validate JSON before saving.
        data = json.loads(content)

        # Save formatted JSON to disk.
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

    def imagine(self, theme: str, filename: str) -> None:
        """
        Generate and save an interactive story.

        This method orchestrates the complete workflow:

        1. Generate the story JSON using Gemini.
        2. Validate the generated content.
        3. Save the result to disk.

        Parameters
        ----------
        theme : str
            Theme used to generate the story.
        filename : str
            Output file path.
        """
        
        attempts = 0

        while attempts <= 5:
            try:
                json_content = self.generate_story_json(theme)
                self.save_json(json_content, filename)
                print(f"Story file saved at: {filename}")
                break

            except ServerError:
                print(
                    "This model is currently experiencing high demand. "
                    "Spikes in demand are usually temporary."
                )

                attempts += 1

                if attempts <= 5:
                    print("Trying again in 5 seconds...")
                    sleep(5)

        else:
            print(
                "This model is currently experiencing high demand. "
                "Spikes in demand are usually temporary. "
                "Please try again later."
            )