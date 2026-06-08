import pandas as pd
import ast

class Pages(object):

    def __init__(self, story_path):
        self.story_path = story_path
        self.story_data = pd.read_csv(self.story_path)
        self.story_data.set_index('id', inplace=True)
        

    def get_options(self, page_id):

        options = ast.literal_eval(self.story_data.loc[page_id, 'options'])

        if len(options) == 0:
            option_list =[]
            options = None
        else:    
            option_list = []
            for option in options:
                option_list.extend(option.keys())
        
        return option_list, options
    
    def get_page_text(self, page_id):

        text = self.story_data.loc[page_id, 'text']
        return text
    

if __name__ == "__main__":
    # pages = Pages("gen-adventure/deadpool.csv")
    # print()

    # print(pages.get_page_text(1))
    # print()

    # print(pages.get_options(1))

    pages = Pages("gen_adventure/detective.csv")

    print(pages.story_data.index[:5])
    print(type(pages.story_data.index[0]))

    print(1 in pages.story_data.index)
    print("1" in pages.story_data.index)