import pandas as pd
import json

class Pages(object):

    def __init__(self, story_path):
        self.story_path = story_path
        self.story_data = {}
        
        with open(self.story_path, 'r', encoding='utf-8') as f:
            self.story_data = json.load(f)
        
    
    def get_options(self, page_id):

        options = self.story_data['pages'][page_id-1]['options']

        if len(options) == 0:
            option_list =[]
            options = None
        else:    
            option_list = []
            for option in options:
                option_list.append(option['text'])
        
        return option_list, options
    
    def get_target_by_text(self, page_id, button_text):
        for option_dict in self.story_data['pages'][page_id -1]['options']:
            if button_text == option_dict['text']:
                return option_dict['target']
    
    def get_page_text(self, page_id):

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