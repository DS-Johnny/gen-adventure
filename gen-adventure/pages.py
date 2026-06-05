import pandas as pd

class Pages(object):

    def __init__(self, story_path):
        self.story_path = story_path
        self.story_data = pd.read_csv(self.story_path)
        pass

    def get_options(self, id):

        options = eval(self.story_data[self.story_data['id'] == id]['options'].values[0])

        if len(options) == 0:
            option_list =[]
            options = None
        else:    
            option_list = []
            for option in options:
                for key, value in option.items():
                    option_list.append(key)
        
        return option_list, options
    

if __name__ == "__main__":
    pages = Pages("gen-adventure/deadpool.csv")

    print(pages.get_options(1))