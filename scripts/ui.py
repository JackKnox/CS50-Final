import pygame

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
        self.outline_col = -1
        self.outline((0, 0, 0))
        self.antialias(False)
        self.starting_format("main-font", "WHITE")
        self.align("TOP_LEFT")

    def starting_format(self, font, color):
        self.color = color
        self.font = font
        self.font_size = self.get_font_asset().size("H")  # Approximate height
        return self

    def get_font_asset(self):
        return self.game.fonts[self.font]

    def align(self, alignment):
        self.offset = ALIGNMENTS.get(alignment, (0, 0))
        return self

    def antialias(self, antialias):
        self.anti_alias = antialias
        return self

    def outline(self, outline_col):
        self.outline_col = outline_col
        return self

    def get_segments(self):
        self.tag_map = []
        text = self.text.split("[")

        if text[0]:
            self.tag_map.append([self.color, text[0]])

        for segment in text[1:]:
            segment_txt = segment.split("]")

            self.tag_map.append((segment_txt[0], segment_txt[1]))

    def get_formatted_text(self):
        text = self.text.split("[")

        new_text = ''

        if text[0]:
            new_text += text[0]

        for segment in text[1:]:
            segment_txt = segment.split("]")

            new_text += segment_txt[1]

        return new_text

    def get_dims(self):
        font = self.game.fonts[self.font]

        height = (self.text.count('\n')+1) * self.font_size[1]
        width = font.size(max(self.get_formatted_text().split('\n'), key=len))[0]
        
        return (width, height)

    def draw(self, x, y):
        self.get_segments()
        text_x, text_y = x, y

        font = self.game.fonts[self.font]
        width, height = self.get_dims()

        for segment in self.tag_map:
            color_tag, text = segment
            color = COLORS.get(color_tag, COLORS["WHITE"])
            newline = False

            if text[-1:] == '\n':
                text = text[:-1] # Set text before font.size()
                newline = True

            text_width, text_height = font.size(text)
            aligned_x = text_x - width * self.offset[0]
            aligned_y = text_y - height * self.offset[1]

            if newline:
                text_y += text_height
            else:
                text_x += text_width

            if self.outline_col != -1:
                directions = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]

                for dir in directions:
                    text_surf = font.render(text, self.anti_alias, self.outline_col)
                    self.game.display.blit(text_surf, (aligned_x-dir[0], aligned_y-dir[1]))

            text_surf = font.render(text, self.anti_alias, color)
            self.game.display.blit(text_surf, (aligned_x, aligned_y))

        return self

class Button(Text):
    def __init__(self, game, text, onclick):
        self.onclick = onclick
        super().__init__(game, text)
    
    def draw(self, x, y):
        width, height = self.get_dims()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        aligned_x = x - width * self.offset[0]
        aligned_y = y - height * self.offset[1]

        width *= self.game.screen_scale
        height *= self.game.screen_scale
        aligned_x *= self.game.screen_scale
        aligned_y *= self.game.screen_scale

        #TODO: Add mouse click (1=left, 3=right) pygame.mouse.get_pressed()
        rect = pygame.Rect(aligned_x, aligned_y, width, height)
        if rect.collidepoint(mouse_x, mouse_y):
            self.color = self.onclick(self)

        return super().draw(x, y)