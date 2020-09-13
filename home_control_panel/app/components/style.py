from types import SimpleNamespace


class Style:
    # Unit
    unit = 1.0  # 384px for 4k
    # Dark Colour Theme
    dark = open('assets/styles/dark.css', 'r').read()
    # Light Colour Theme
    light = open('assets/styles/light.css', 'r').read()
    # Colours
    colors = SimpleNamespace()
    # Text
    text = SimpleNamespace()
    # Text
    sizes = SimpleNamespace()
    # Dark Colour
    colors.dark = '#191919'  # other #0f131a
    # Dark Colour
    colors.dark_alt = '#0F0F0F'
    # Dark Colour
    colors.dark_text = '#888888'
    # Light Colour
    colors.light = '#141414'  # other #1a1d24
    # Light Colour
    colors.light_alt = '#1C1A1A'
    # Light Colour
    colors.light_text = '#dedede'
    # Highlight Colour
    colors.highlight = '#81D4FA'
    # Highlight Text Colour
    colors.highlight_text = '#98C8DE'
    # Header Text
    text.head = '1px'
    # Sub Header Text
    text.subhead = '1px'
    # Button text
    text.button = '1px'
    # Label text
    text.label = '1px'
    # Small text
    text.small = '1px'
    # Font
    text.font = 'Corbel, sans-serif'
    # Border
    sizes.border_thick = 2
    # Border
    sizes.border_thin = 1
    # Radius
    sizes.radius_large = 1
    # Radius
    sizes.radius_medium = 1
    # Radius
    sizes.radius_small = 1
    # Icons
    sizes.icon_logo = 1
    # Icons
    sizes.icon_large = 1
    # Icons
    sizes.icon_medium = 1
    # Icons
    sizes.icon_small = 1
    # Margin
    sizes.margin_large = 1
    # Margin
    sizes.margin_medium = 1
    # Margin
    sizes.margin_small = 1
    # Padding
    sizes.padding_large = 1
    # Padding
    sizes.padding_medium = 1
    # Padding
    sizes.padding_small = 1

    @staticmethod
    def get_unit(multiplier=1.0):
        return Style.unit * multiplier

    @staticmethod
    def set_unit(dimensions):
        (Style.screen_width, Style.screen_height) = dimensions
<<<<<<< Updated upstream
        Style.unit = (Style.screen_width / 2) / 4  # 384px
        Style.width = 5.5 * Style.unit
        Style.height = 3 * Style.unit
        Style.h_margin = int((Style.screen_width - Style.width) / 2)
        Style.v_margin = int((Style.screen_height - Style.height) / 2)
        Style.text.head = str(int(Style.unit / 8.4)) + 'px'  # 60px
        Style.text.subhead = str(int(Style.unit / 10.67)) + 'px'  # 36px
        Style.text.button = str(int(Style.unit / 21.33)) + 'px'  # 18px
        Style.text.label = str(int(Style.unit / 21.33)) + 'px'  # 18px
        Style.text.small = str(int(Style.unit / 24.0)) + 'px'  # 18px

        Style.sizes.radius_large = int(Style.unit / 12.8)  # 30px
        Style.sizes.radius_medium = int(Style.unit / 19.2)  # 20px
        Style.sizes.radius_small = int(Style.unit / 25.6)  # 15px
=======
        Style.unit = max(min(Style.screen_width / 3.8 / 3.5, 480), 80)  # 480px
        Style.width = 3.5 * Style.unit
        Style.height = 2 * Style.unit
        Style.h_margin = int((Style.screen_width - Style.width) / 2)
        Style.v_margin = int((Style.screen_height - Style.height) / 2)
        Style.text.head = str(int(Style.unit / 7)) + 'px'  # 60px
        Style.text.subhead = str(int(Style.unit / 14.5)) + 'px'  # 36px
        Style.text.button = str(int(Style.unit / 15.5)) + 'px'  # 18px
        Style.text.label = str(int(Style.unit / 15.5)) + 'px'  # 18px
        Style.text.small = str(int(Style.unit / 16)) + 'px'  # 18px

        Style.sizes.radius_large = int(Style.unit / 36)  # 30px
        Style.sizes.radius_medium = int(Style.unit / 50)  # 20px
        Style.sizes.radius_small = int(Style.unit / 60)  # 15px
>>>>>>> Stashed changes
        Style.sizes.icon_logo = int(Style.unit * 0.6)
        Style.sizes.icon_large = int(Style.unit / 6)
        Style.sizes.icon_medium = int(Style.unit / 10)
        Style.sizes.icon_small = int(Style.unit / 18)

<<<<<<< Updated upstream
        Style.sizes.border_thick = int(Style.unit / 380)  # 2
=======
        Style.sizes.border_thick = max(int(Style.unit / 420), 1)  # 2
>>>>>>> Stashed changes
        Style.sizes.border_thin = 1  # 1

        Style.sizes.margin_large = int(Style.unit / 10.97)  # 35
        Style.sizes.margin_medium = int(Style.unit / 25.6)  # 15
        Style.sizes.margin_small = int(Style.unit / 76.8)  # 5
        Style.sizes.padding_large = int(Style.unit / 25.6)  # 15
        Style.sizes.padding_medium = int(Style.unit / 38.4)  # 10
        Style.sizes.padding_small = int(Style.unit / 192)  # 2

        Style.update_styles()

    @staticmethod
    def update_styles():
        Style.dark = Style.replace_variables(Style.dark)
        Style.light = Style.replace_variables(Style.light)

    @staticmethod
    def replace_variables(text):
        text = text.replace('@None', '0px')
        text = text.replace('@UnitSize', str(Style.unit))

        text = text.replace('@DarkColor', Style.colors.dark)
        text = text.replace('@AltDarkColor', Style.colors.dark_alt)
        text = text.replace('@LightColor', Style.colors.light)
        text = text.replace('@AltLightColor', Style.colors.light_alt)
        text = text.replace('@HighlightColor', Style.colors.highlight)
        text = text.replace('@HighlightTextColor', Style.colors.highlight_text)
        text = text.replace('@DarkTextColor', Style.colors.dark_text)
        text = text.replace('@LightTextColor', Style.colors.light_text)

        text = text.replace('@HeadTextSize', Style.text.head)
        text = text.replace('@SubTextSize', Style.text.subhead)
        text = text.replace('@ButtonTextSize', Style.text.button)
        text = text.replace('@LabelTextSize', Style.text.label)
        text = text.replace('@SmallTextSize', Style.text.small)
        text = text.replace('@TextFont', Style.text.font)

        text = text.replace('@LargeRadius', str(Style.sizes.radius_large) + 'px')
        text = text.replace('@MediumRadius', str(Style.sizes.radius_medium) + 'px')
        text = text.replace('@SmallRadius', str(Style.sizes.radius_small) + 'px')

        text = text.replace('@LogoSize', str(Style.sizes.icon_logo) + 'px')
        text = text.replace('@LargeIconSize', str(Style.sizes.icon_large) + 'px')
        text = text.replace('@MediumIconSize', str(Style.sizes.icon_medium) + 'px')
        text = text.replace('@SmallIconSize', str(Style.sizes.icon_small) + 'px')

        text = text.replace('@BorderThick', str(Style.sizes.border_thick) + 'px')
        text = text.replace('@BorderThin', str(Style.sizes.border_thin) + 'px')

        text = text.replace('@LargeMargin', str(Style.sizes.margin_large) + 'px')
        text = text.replace('@MediumMargin', str(Style.sizes.margin_medium) + 'px')
        text = text.replace('@SmallMargin', str(Style.sizes.margin_small) + 'px')

        text = text.replace('@LargePadding', str(Style.sizes.padding_large) + 'px')
        text = text.replace('@MediumPadding', str(Style.sizes.padding_medium) + 'px')
        text = text.replace('@SmallPadding', str(Style.sizes.padding_small) + 'px')

        return text
