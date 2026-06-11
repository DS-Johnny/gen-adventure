import json

class Pages(object):
    """
    Manage story data and provide methods for retrieving page content,
    available options, and navigation targets.

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
        Load the story data from a JSON file.

        Parameters
        ----------
        story_path : str
            Path to the JSON file containing the story structure.
        """
        self.story_path = story_path
        self.story_data = {}
        
        # Load the complete story into memory.
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
    

if __name__ == "__main__":
    pages = Pages("gen_adventure/formatura.json")
    print()

    print(pages.get_page_text(1))
    print()

    print(pages.get_options(1))

    # pages = Pages("gen_adventure/.csv")

    # print(pages.story_data.index[:5])
    # print(type(pages.story_data.index[0]))

    # print(1 in pages.story_data.index)
    # print("1" in pages.story_data.index)