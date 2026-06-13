# Gen-Adventure

Generate and play AI-powered interactive adventures with Python, Pygame, and Google Gemini.

Gen-Adventure allows you to:

* Create interactive branching stories using Google's Gemini models.
* Play generated stories through a graphical interface built with Pygame.
* Load stories from local JSON files or remote URLs.
* Explore built-in example adventures.

---

## Features

* AI-powered story generation using Gemini.
* Interactive branching adventures.
* Pygame graphical interface.
* Local and remote story support.
* JSON-based story format.
* Built-in example stories.

---

## Installation

```bash
pip install gen-adventure
```

---

## Requirements

* Python 3.11+
* Google Gemini API Key

---

## Playing an Adventure

Load a local JSON story:

```python
from gen_adventure import Adventure

game = Adventure("my_story.json")
game.start()
```

Load a story hosted online:

```python
from gen_adventure import Adventure

game = Adventure(
    "https://example.com/my_story.json"
)

game.start()
```

---

## Built-in Example Stories

Gen-Adventure includes several example stories hosted in the project's repository.

```python
from gen_adventure import Adventure, StoryExamples

examples = StoryExamples()

game = Adventure(examples.fantasy)
game.start()
```

Available examples:

* fantasy
* hacker
* formatura
* love_story

---

## Generating Stories with Gemini

Create a story and save it as a JSON file:

```python
from gen_adventure import StoryImaginator

imaginator = StoryImaginator("YOUR_GEMINI_API_KEY")

imaginator.imagine(
    "A cyberpunk hacker fighting an evil corporation",
    "cyberpunk_story.json"
)
```
Standard Gemini model is 'gemini-2.5-flash', but you can change into another model you prefer.
Changing Gemini model:

```python
from gen_adventure import StoryImaginator

imaginator = StoryImaginator("YOUR_GEMINI_API_KEY")
imaginator.model = "gemini-3.5-flash"

```



The generated file can then be loaded into the game:

```python
from gen_adventure import Adventure

game = Adventure("cyberpunk_story.json")
game.start()
```




---

## Story Format

Stories are stored as JSON files.

Example:

```json
{
    "pages": [
        {
            "id": 1,
            "text": "You wake up in a mysterious forest.",
            "options": [
                {
                    "text": "Follow the path",
                    "target": 2
                },
                {
                    "text": "Enter the cave",
                    "target": 3
                }
            ]
        }
    ]
}
```

Each page contains:

| Field   | Description       |
| ------- | ----------------- |
| id      | Page identifier   |
| text    | Story content     |
| options | Available choices |

Each option contains:

| Field  | Description                  |
| ------ | ---------------------------- |
| text   | Text displayed to the player |
| target | Destination page             |

---

## Customizing Colors

You can customize the interface colors:

```python
from gen_adventure import Adventure

game = Adventure("story.json")

game.text_color = (255, 255, 255)
game.background_color = (25, 25, 25)
game.button_background_color = (50, 50, 50)

game.start()
```

---

## Example Workflow

Generate a story:

```python
from gen_adventure import StoryImaginator

imaginator = StoryImaginator("YOUR_GEMINI_API_KEY")

imaginator.imagine(
    "A medieval knight searching for a lost kingdom",
    "kingdom.json"
)
```

Play the generated adventure:

```python
from gen_adventure import Adventure

game = Adventure("kingdom.json")
game.start()
```

---

## Project Structure

```text
gen_adventure/
├── adventure.py
├── pages.py
├── story_imaginator.py
└── __init__.py
```

---

## Dependencies

* pygame
* google-genai
* requests

---

## License

This project is licensed under the MIT License.

See the LICENSE file for details.

---

## Author

Johnny Matos

GitHub: https://github.com/DS-Johnny
