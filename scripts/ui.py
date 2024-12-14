ALIGNMENTS = {
    "TOP_LEFT": (0, 0),
    "TOP_RIGHT": (1, 0),
    "TOP_CENTER": (0.5, 0),
    "MIDDLE_LEFT": (0, 0.5),
    "MIDDLE_RIGHT": (1, 0.5),
    "MIDDLE_CENTER": (0.5, 0.5),
    "BOTTOM_LEFT": (0, 1),
    "BOTTOM_RIGHT": (1, 1),
    "BOTTOM_CENTER": (0.5, 1),
}

COLORS = {
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
}

class Text:
    def __init__(self, game, text):
        self.game = game.game
        self.text = text
        self.tag_map = []
        self.antialias(False)
        self.starting_format("main-font", COLORS["WHITE"])
        self.align("TOP_LEFT")

    def starting_format(self, font, color):
        self.color = color
        self.font = font
        self.font_size = self.game.fonts[self.font].size("H")  # Approximate height
        return self

    def align(self, alignment):
        self.offset = ALIGNMENTS.get(alignment, (0, 0))
        return self

    def antialias(self, antialias):
        self.anti_alias = antialias
        return self

    def get_segments(self):
        self.tag_map = []
        segments = self.text.split("[")
        for segment in segments[1:]:
            if "]" in segment:
                tag, content = segment.split("]", 1)
                lines = content.split("\n")  # Split by newline
                for line in lines:
                    self.tag_map.append((tag.strip(), line.strip()))
            else:
                # Handle malformed tags gracefully
                self.tag_map.append(("WHITE", segment.strip()))

    def draw(self, x, y):
        self.get_segments()
        initial_x, initial_y = x, y  # Save starting position

        for segment in self.tag_map:
            color_tag, text = segment
            color = COLORS.get(color_tag, COLORS["WHITE"])
            font = self.game.fonts[self.font]

            text_width, text_height = font.size(text)
            aligned_x = initial_x - text_width * self.offset[0]
            aligned_y = y - text_height * self.offset[1]

            # Render the text
            text_surf = font.render(text, self.anti_alias, color)
            self.game.display.blit(text_surf, (aligned_x, aligned_y))

            # Move to the next line for multiline text
            y += text_height/2

        return self
