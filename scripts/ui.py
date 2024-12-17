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

#TODO: Add base colours and colour pallette 
COLORS = {
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "GREEN" : (0, 255, 0)
}

class Text:
    def __init__(self, game, text):
        self.game = game.game
        self.text = text
        self.tag_map = []
        self.antialias(False)
        self.starting_format("main-font", "WHITE")
        self.align("TOP_LEFT")

    def starting_format(self, font, color):
        self.color = color
        self.font = font
        self.font_size = self.get_font_asset().size("H")  # Approximate height
        self.space = self.get_font_asset().size(" ")[0]
        return self

    def get_font_asset(self):
        return self.game.fonts[self.font]

    def align(self, alignment):
        self.offset = ALIGNMENTS.get(alignment, (0, 0))
        return self

    def antialias(self, antialias):
        self.anti_alias = antialias
        return self

    def get_segments(self):
        self.tag_map = []
        text = self.text.split("[")

        if text[0]:
            self.tag_map.append(["WHITE", text[0]])

        for segment in text[1:]:
            segment_txt = segment.split("]")

            self.tag_map.append((segment_txt[0], segment_txt[1]))

    def draw(self, x, y):
        self.get_segments()
        text_x, text_y = x, y

        for segment in self.tag_map:
            color_tag, text = segment
            color = COLORS.get(color_tag, COLORS["WHITE"])
            font = self.game.fonts[self.font]
            newline = False

            if text[-1:] == '\n':
                text = text[:-1] # Set text before font.size()
                newline = True

            width, height = font.size(text)
            aligned_x = text_x - width * self.offset[0]
            aligned_y = text_y - height * self.offset[1]

            if newline:
                text_y += height
            else:
                text_x += width + self.space
            
            text_surf = font.render(text, self.anti_alias, color)
            self.game.display.blit(text_surf, (aligned_x, aligned_y))

        return self
