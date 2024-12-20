import pygame

CONTAINER_SPACE = -1

TOP_LEFT = (0, 0)
TOP_RIGHT = (1, 0)
TOP_CENTER = (0.5, 0)
MIDDLE_LEFT = (0, 0.5)
MIDDLE_RIGHT = (1, 0.5)
MIDDLE_CENTER = (0.5, 0.5)
BOTTOM_LEFT = (0, 1)
BOTTOM_RIGHT = (1, 1)
BOTTOM_CENTER = (0.5, 1)

PALETTE_WOOD = (190, 74, 47)
PALETTE_LIGHT_WOOD = (215, 118, 67)
PALETTE_CREAM = (234, 212, 170)
PALETTE_DARK_CREAM = (228, 166, 114)
PALETTE_LIGHT_BROWN = (184, 111, 80)
PALETTE_BROWN = (115, 62, 57)
PALETTE_DARK_BROWN = (62, 39, 49)
PALETTE_MAHOGANY = (162, 38, 51)
PALETTE_LIGHT_RED = (228, 59, 68)
PALETTE_ORANGE = (247, 118, 34)
PALETTE_LIGHT_ORANGE = (254, 174, 52)
PALETTE_YELLOW = (254, 231, 97)
PALETTE_LIGHT_GREEN = (99, 199, 77)
PALETTE_GREEN = (62, 137, 72)
PALETTE_DARK_GREEN = (38, 92, 66)
PALETTE_VERY_DARK_GREEN = (25, 60, 62)
PALETTE_DARK_BLUE = (18, 78, 137)
PALETTE_BLUE = (0, 153, 219)
PALETTE_LIGHT_BLUE = (44, 232, 245)
PALETTE_WHITE = (255, 255, 255)
PALETTE_LIGHT_GREY = (192, 203, 220)
PALETTE_GREY = (139, 155, 180)
PALETTE_DARK_GREY = (90, 105, 136)
PALETTE_VERY_DARK_GREY = (58, 68, 102)
PALETTE_LIGHT_BLACK = (38, 43, 68)
PALETTE_BLACK = (24, 20, 37)
PALETTE_RED = (255, 0, 68)
PALETTE_PURPLE = (104, 56, 108)
PALETTE_MAGENTA = (181, 80, 136)
PALETTE_PINK = (246, 117, 122)
PALETTE_SKIN = (232, 183, 150)
PALETTE_DARK_SKIN = (194, 133, 105)

class Text:
    def __init__(self, game, text):
        self.game = game.game
        self.text = text
        self.tag_map = []
        self.outline_col = -1
        self.outline((0, 0, 0))
        self.antialias(False)
        self.starting_format("main-font", PALETTE_WHITE)
        self.align(TOP_LEFT)
        self.scale(2)

    def starting_format(self, font, color):
        self.color = color
        self.font = font
        self.font_size = self.get_font_asset().size("H")  # Approximate height
        return self

    def get_font_asset(self):
        return self.game.fonts[self.font]

    def align(self, alignment):
        self.offset = alignment
        return self

    def antialias(self, antialias):
        self.anti_alias = antialias
        return self

    def outline(self, outline_col):
        self.outline_col = outline_col
        return self

    def scale(self, scale):
        self.text_scale = scale

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

        height = (self.text.count('\n')+1) * self.font_size[1] * self.text_scale
        width = font.size(max(self.get_formatted_text().split('\n'), key=len))[0] * self.text_scale
        
        return (width, height)

    def draw(self, x, y):
        self.get_segments()
        text_x, text_y = x, y

        font = self.game.fonts[self.font]
        width, height = self.get_dims()

        for segment in self.tag_map:
            color, text = segment
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
                    text_surf = pygame.transform.scale(text_surf, (text_surf.get_width() * self.text_scale, text_surf.get_height() * self.text_scale))
                    self.game.display.blit(text_surf, (aligned_x-dir[0], aligned_y-dir[1]))

            text_surf = font.render(text, self.anti_alias, color)
            text_surf = pygame.transform.scale(text_surf, (text_surf.get_width() * self.text_scale, text_surf.get_height() * self.text_scale))
            self.game.display.blit(text_surf, (aligned_x, aligned_y))

        return self

class Button(Text):
    def __init__(self, game, text, onclick, hover_col=PALETTE_RED):
        self.onclick = onclick
        self.hover_col = hover_col
        super().__init__(game, text)

    def starting_format(self, font, color):
        self.unhover_col = color
        return super().starting_format(font, color)
    
    def draw(self, x, y):
        width, height = self.get_dims()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        aligned_x = x - width * self.offset[0]
        aligned_y = y - height * self.offset[1]

        width *= self.game.screen_scale
        height *= self.game.screen_scale
        aligned_x *= self.game.screen_scale
        aligned_y *= self.game.screen_scale

        rect = pygame.Rect(aligned_x, aligned_y, width, height)
        buttons = pygame.mouse.get_pressed()
        on_hover = (rect.collidepoint(mouse_x, mouse_y))
        
        self.color = self.hover_col if on_hover else self.unhover_col

        if on_hover and buttons[0]:
            self.onclick(self)

        return super().draw(x, y)
    
class Container:
    def __init__(self, game, layout):
        self.game = game.game
        self.layout = layout

        self.space = Text(self, " ")

        self.outline((0, 0, 0), False)
        self.antialias(False, False)
        self.starting_format("main-font", PALETTE_WHITE, False)
        self.align(TOP_LEFT) # Dont sync alignment, do it manually
        self.scale(1)
        self.sync_settings()

    def sync_settings(self):
        for ele in self.layout:
            if ele == CONTAINER_SPACE:
                ele = self.space
            ele.outline(self.outline_col)
            ele.antialias(self.anti_alias)
            ele.starting_format(self.font, self.color)
            ele.align(self.offset)
            ele.scale(self.text_scale)

    def starting_format(self, font, color, sync=True):
        self.color = color
        self.font = font
        self.font_size = self.get_font_asset().size("H")  # Approximate height

        if sync:
            self.sync_settings()

        return self

    def get_font_asset(self):
        return self.game.fonts[self.font]

    def align(self, alignment):
        self.offset = alignment

        return self

    def antialias(self, antialias, sync=True):
        self.anti_alias = antialias

        if sync:
            self.sync_settings()

        return self

    def outline(self, outline_col, sync=True):
        self.outline_col = outline_col

        if sync:
            self.sync_settings()

        return self
    
    def get_dims(self):
        font = self.game.fonts[self.font]

        height = self.font_size[1] * len(self.layout)* self.text_scale
        width = font.size(max([self.space.get_formatted_text() if ele == CONTAINER_SPACE else ele.get_formatted_text() for ele in self.layout], key=len))[0] * self.text_scale
        
        return (width, height)

    def scale(self, scale):
        self.text_scale = scale

    def draw(self, x, y):
        text_x, text_y = x, y
        width, height = self.get_dims()

        for ele in self.layout:
            if ele == CONTAINER_SPACE:
                ele = self.space

            ele_width, ele_height = ele.get_dims()
            aligned_x = (text_x - width * self.offset[0]) + (width - ele_width) / 2
            aligned_y = (text_y - height * self.offset[1])

            ele.draw(aligned_x, aligned_y)

            text_y += ele_height