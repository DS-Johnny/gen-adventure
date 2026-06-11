import pygame
from pygame.locals import *
from pages import Pages



class Adventure(object):
    """
    Main game controller responsible for managing the application window,
    page navigation, user interface elements, and game state.

    Parameters
    ----------
    story_path : str
        Path to the story file used to load the interactive adventure.
    """
        
    def __init__(self, story_path:str) -> None:
        """
        Initialize the game window, visual settings, page manager,
        fonts, buttons, and screen state variables.

        Parameters
        ----------
        story_path : str
            Path to the story file that will be loaded by the Pages class.
        """
        pygame.init()
        pygame.display.set_caption('Gen-Adventure')

        # Initialize the page manager responsible for loading
        # and handling story content.
        self.pages = Pages(story_path)


        # Window configuration
        self.WINDOW_WIDTH = 1200
        self.WINDOW_HEIGHT = 1000
        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        # # Color palette used throughout the application.
        self.text_color = (254, 250, 224)
        self.background_color = (96, 108, 56)
        self.button_background_color = (40, 54, 24)

        # Variables used to control the current screen and page state.
        self.__end_screen = False
        self.__start_screen = True
        self.__page = 1
        self.__page_text = ''
        
        # Default font and rectangle used by static buttons.
        self.__font = pygame.font.SysFont(None, 36)
        self.__button_rect = pygame.Rect((self.WINDOW_WIDTH - 200) //2, (self.WINDOW_HEIGHT -200 //2), 200, 50)

        # Font and rendered surface used to display page text.
        self.font_page_text = pygame.font.SysFont('rasa', 30)
        self.page_text = self.font_page_text.render(self.__page_text, True, self.text_color)

        # Stores the text labels for dynamically generated option buttons.
        self.__option_list = []

        # Stores the pygame.Rect objects associated with dynamic buttons.
        self.__buttons = []


    def draw_multiline_text(self, text: str, font: pygame.font.Font, color: tuple, x: int, y: int, max_width:int) -> None:
        """
        Render and display multiline text inside a maximum width.

        The text is automatically wrapped by splitting it into words and
        creating new lines whenever the current line exceeds the specified
        width.

        Parameters
        ----------
        text : str
            Text to be rendered.
        font : pygame.font.Font
            Font used to render the text.
        color : tuple
            RGB color of the rendered text.
        x : int
            Horizontal starting position.
        y : int
            Vertical starting position.
        max_width : int
            Maximum width allowed before wrapping to a new line.
        """
        words = text.split(' ')
        line = ''
        y_offset = 0

        # Build each line word by word until the maximum width is reached.
        for word in words:
            new_line = line + word + ' '
            tamanho_linha, _ = font.size(new_line)
            
            # Render the current line and move to the next one
            # when the maximum width is exceeded.
            if tamanho_linha > max_width:
                rendered_line = font.render(line, True, color)
                self.window.blit(rendered_line, (x, y + y_offset))
                y_offset += font.get_height() + 5
                line = word + ' '
            else:
                line = new_line

        # Render the remaining text after the loop finishes.
        if line:
            rendered_line = font.render(line, True, color)
            self.window.blit(rendered_line, (x, y + y_offset))

    def draw_button(self, text: str):
        """
        Draw a button with centered text on the game window.

        The button uses the predefined rectangle, background color,
        and font configured during initialization.

        Parameters
        ----------
        text : str
            Label displayed inside the button.
        """
        # Draw the button background.
        pygame.draw.rect(self.window, self.button_background_color, self.__button_rect)

        # Render the button label.
        text_img = self.__font.render(text, True, self.text_color)

        # Center the text inside the button rectangle.
        text_rect = text_img.get_rect(center=self.__button_rect.center)

        # Draw the text on the screen.
        self.window.blit(text_img, text_rect)

    # Create dynamic buttons based on the current page options.
    def create_buttons(self) -> None:
        """
        Create and position the dynamic option buttons displayed on screen.

        The buttons are generated from the entries stored in
        ``self.__option_list``. Each button is represented by a tuple
        containing a pygame.Rect and its associated text label.

        Existing buttons are cleared before new ones are created.
        """

        # Remove previously generated buttons.
        self.__buttons.clear()

        width = 1200
        height = 40
        space = 20
        y_inicial = 800

        # Left position of the button group.
        x = 0 #(self.WINDOW_WIDTH - 600) //2

        # Create a button rectangle for each available option.
        for i, text in enumerate(self.__option_list):
            y = y_inicial + i * (height + space)
            rect = pygame.Rect(x, y, width, height)

            # Store the button rectangle together with its label.
            self.__buttons.append((rect, text))

    # Draw all dynamic option buttons.
    def draw_buttons(self) -> None:
        """
        Draw all dynamically generated buttons on the screen.

        Each button consists of a background rectangle and a centered
        text label stored in ``self.__buttons``.
        """

        for rect, text in self.__buttons:

            # Draw the button background.
            pygame.draw.rect(self.window, self.button_background_color, rect)

            # Render and center the button label.
            texto_img = self.__font.render(text, True, self.text_color)
            texto_rect = texto_img.get_rect(center=rect.center)

            # Draw the label on the screen.
            self.window.blit(texto_img, texto_rect)

    def game_over(self) -> None:
        """
        Display the game over screen.

        Renders the ending message and a restart button, allowing the
        player to begin a new adventure.
        """
        end_font = pygame.font.SysFont('rasa', 40)
        self.draw_multiline_text('The end!', end_font, self.text_color, 530, 850, 600)
        self.draw_button('Restart')
            
            
    def start(self) -> None:
        """
        Start and run the main game loop.

        This method handles:

        - Window rendering.
        - User input processing.
        - Page navigation.
        - Dynamic button creation.
        - Story progression.
        - Start and ending screens.

        The loop runs continuously until the application is closed.
        """
        
        self.create_buttons()
        while True:
            
            # Clear the screen before rendering a new frame.
            self.window.fill(self.background_color)

            # Process user input events.
            for event in pygame.event.get():

                # Close the application when the window is closed.
                if event.type == QUIT:
                    pygame.quit()
                    quit()    

                # Handle mouse clicks.
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # Handle clicks on the main action button
                    # (Start / Restart).
                    if self.__button_rect.collidepoint(event.pos):
                        
                        if self.__start_screen:
                            self.__start_screen = False    
                        elif self.__end_screen:
                            self.__page = 1
                            self.__start_screen = True
                            self.__end_screen = False
                    
                    # Handle clicks on story option buttons.
                    if not self.__start_screen:
                        for i, (rect, text) in enumerate(self.__buttons):
                            if rect.collidepoint(event.pos):
                                print(f"You chose: {text}")
                                self.__page = self.pages.get_target_by_text(self.__page, text)

            # Render the start screen.
            if self.__start_screen:

                self.draw_button("Start")

            else:
                
                # Display the current page content.
                page_text = self.pages.get_page_text(self.__page)

                self.draw_multiline_text(page_text, self.font_page_text, self.text_color, (self.WINDOW_WIDTH) //4, 200, 600)

                # Load and display available choices for the current page.
                self.__option_list, options_dict = self.pages.get_options(self.__page)
                
                self.create_buttons()
                self.draw_buttons()

                # If no choices remain, display the ending screen.
                if len(self.__option_list) == 0:
                    self.game_over()
                    self.__end_screen = True 
    
            # Update the display with the newly rendered frame.
            pygame.display.flip()


if __name__ == "__main__":
    # adventure = Adventure("gen_adventure/formatura.json")
    adventure = Adventure("gen_adventure/fantasy.json")
    
    adventure.start()