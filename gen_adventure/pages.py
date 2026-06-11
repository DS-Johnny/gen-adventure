"""
Manage story data loaded from a JSON file.

Expected JSON structure:

{
    "pages": [
        {
            "id": 1,
            "text": "...",
            "options": [
                {
                    "text": "...",
                    "target": 2
                }
            ]
        }
    ]
}
"""

import json
import requests

class Pages(object):
    """
    Manage story data and provide methods for retrieving page content,
    available options, and navigation targets.

    Story data can be loaded either from a local JSON file or from a
    remote JSON resource accessible through an HTTP/HTTPS URL.

    The story is loaded from a JSON file during initialization and
    stored in memory for quick access throughout the game.

    Expected JSON structure:

    {
        "pages": [
            {
                "id": 1,
                "text": "...",
                "options": [
                    {
                        "text": "...",
                        "target": 2
                    }
                ]
            }
        ]
    }


    """

    def __init__(self, story_path: str) -> None:
        """
        Load story data from a local JSON file or a remote URL.

        Parameters
        ----------
        story_path : str
            Local file path or HTTP/HTTPS URL pointing to a story JSON file.
        """
        self.story_path = story_path
        self.story_data = {}
        
        # Load the complete story into memory.
        if self.story_path.startswith("http"):
            
            # Download story data from a remote JSON resource.
            response = requests.get(self.story_path)
            response.raise_for_status()
            
            self.story_data = response.json()

        else:

            # Load story data from a local JSON file.
            with open(self.story_path, 'r', encoding='utf-8') as f:
                self.story_data = json.load(f)
        
    
    def get_options(self, page_id: int) -> tuple[list, list | None]:
        """
        Retrieve all available options for a given page.

        Parameters
        ----------
        page_id : int
            Identifier of the page to retrieve options from.

        Returns
        -------
        tuple[list, list | None]
            A tuple containing:

            - A list of option texts used for button labels.
            - The original option dictionaries or None if no options exist.
        """

        options = self.story_data['pages'][page_id-1]['options']

        if len(options) == 0:
            option_list =[]
            options = None

        else:    
            option_list = []

            # Extract option labels for button creation.
            for option in options:
                option_list.append(option['text'])
        
        return option_list, options
    
    def get_target_by_text(self, page_id: int, button_text: str) -> int:
        """
        Retrieve the target page associated with a selected option.

        Parameters
        ----------
        page_id : int
            Current page identifier.
        button_text : str
            Text displayed on the selected button.

        Returns
        -------
        int
            Identifier of the destination page.
        """
        
        # Find the option matching the selected button text.
        for option_dict in self.story_data['pages'][page_id -1]['options']:

            if button_text == option_dict['text']:
                return option_dict['target']
    
    def get_page_text(self, page_id: int) -> str:
        """
        Retrieve the narrative text for a specific page.

        Parameters
        ----------
        page_id : int
            Identifier of the page to retrieve.

        Returns
        -------
        str
            Narrative content of the requested page.
        """


        text = self.story_data['pages'][page_id-1]['text']
        return text
