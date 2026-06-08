import pygame
from pygame.locals import *
from pages import Pages



class Adventure(object):

    def __init__(self, story_path):
        pygame.init()
        pygame.display.set_caption('Gen-Adventure')

        # Pages
        self.pages = pg = Pages(story_path)


        # Window
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 800
        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        # Colors
        self.text_color = (254, 250, 224)
        self.background_color = (96, 108, 56)
        self.button_background_color = (40, 54, 24)

        # Screen/page Status
        self.__end_screen = False
        self.__start_screen = True
        self.__page = 1
        self.__page_text = ''
        
        # Button font and rect
        self.__font = pygame.font.SysFont(None, 36)
        self.__button_rect = pygame.Rect((self.WINDOW_WIDTH - 200) //2, 600, 200, 50)

        # Page_text font and position
        self.font_page_text = pygame.font.SysFont('rasa', 30)
        self.page_text = self.font_page_text.render(self.__page_text, True, self.text_color)

        # Dinamic Buttons
        # List of button names
        self.__option_list = []

        # Save Button Recs
        self.__buttons = []


    def draw_multiline_text(self, text, font, color, x, y, max_width):
        words = text.split(' ')
        line = ''
        y_offset = 0

        for word in words:
            new_line = line + word + ' '
            tamanho_linha, _ = font.size(new_line)
            if tamanho_linha > max_width:
                rendered_line = font.render(line, True, color)
                self.window.blit(rendered_line, (x, y + y_offset))
                y_offset += font.get_height() + 5
                line = word + ' '
            else:
                line = new_line

        if line:
            rendered_line = font.render(line, True, color)
            self.window.blit(rendered_line, (x, y + y_offset))

    def draw_button(self, text):
        pygame.draw.rect(self.window, self.button_background_color, self.__button_rect)
        text_img = self.__font.render(text, True, self.text_color)
        text_rect = text_img.get_rect(center=self.__button_rect.center)
        self.window.blit(text_img, text_rect)

    # Create dinamic buttons
    def create_buttons(self):
        self.__buttons.clear()
        width = 700
        height = 40
        space = 20
        y_inicial = 600
        x = (800 - width) // 2

        for i, text in enumerate(self.__option_list):
            y = y_inicial + i * (height + space)
            rect = pygame.Rect(x, y, width, height)
            self.__buttons.append((rect, text))

    # Draw buttons
    def draw_buttons(self):
        for rect, text in self.__buttons:
            pygame.draw.rect(self.window, self.button_background_color, rect)
            texto_img = self.__font.render(text, True, self.text_color)
            texto_rect = texto_img.get_rect(center=rect.center)
            self.window.blit(texto_img, texto_rect)

    def game_over(self):
        end_font = pygame.font.SysFont('rasa', 40)
        self.draw_multiline_text('The end!', end_font, self.text_color, 350, 500, 600)
        self.draw_button('Restart')
            
            
    def start(self):
        
        self.create_buttons()
        while True:
            
            self.window.fill(self.background_color)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    quit()    

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.__button_rect.collidepoint(event.pos):
                        
                        if self.__start_screen:
                            self.__start_screen = False    
                        elif self.__end_screen:
                            self.__page = 1
                            self.__start_screen = True
                            self.__end_screen = False

                    if not self.__start_screen:
                        for i, (rect, text) in enumerate(self.__buttons):
                            if rect.collidepoint(event.pos):
                                print(f"You chose: {text}")
                                opcao = options_dict[self.__option_list.index(text)]
                                self.__page = opcao[text]


            if self.__start_screen:
                self.draw_button("Start")

            else:
                # Exibe o primeiro texto e inicia o jogo
                page_text = self.pages.get_page_text(self.__page)
                self.draw_multiline_text(page_text, self.font_page_text, self.text_color, 100, 200, 600)
                self.__option_list, options_dict = self.pages.get_options(self.__page)
                
                self.create_buttons()
                self.draw_buttons()
            
                if len(self.__option_list) == 0:
                    self.game_over()
                    self.__end_screen = True 
    
        
            pygame.display.flip()


if __name__ == "__main__":

    adventure = Adventure("gen_adventure/detective.csv")
    
    adventure.start()