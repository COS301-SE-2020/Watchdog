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
    colors.dark = '#0f131a'
    # Dark Colour
    colors.dark_text = 'white'
    # Light Colour
    colors.light = '#1a1d24'
    # Light Colour
    colors.light_text = 'white'
    # Highlight Colour
    colors.highlight = '#8cbeff'
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
    # Sizes
    sizes.border = '1px'

    @staticmethod
    def get_unit(multiplier=1.0):
        return Style.unit * multiplier

    @staticmethod
    def set_unit(unit):
        Style.unit = unit  # 384px
        Style.text.head = str(int(Style.unit / 6.4)) + 'px'  # 60px
        Style.text.subhead = str(int(Style.unit / 10.67)) + 'px'  # 36px
        Style.text.button = str(int(Style.unit / 21.33)) + 'px'  # 18px
        Style.text.label = str(int(Style.unit / 21.33)) + 'px'  # 18px
        Style.text.small = str(int(Style.unit / 24.0)) + 'px'  # 18px
        Style.update_styles()

    @staticmethod
    def update_styles():
        Style.dark = Style.replace_variables(Style.dark)
        Style.light = Style.replace_variables(Style.light)

    @staticmethod
    def replace_variables(text):
        text = text.replace('@UnitSize', str(Style.unit))
        text = text.replace('@DarkColor', Style.colors.dark)
        text = text.replace('@LightColor', Style.colors.light)
        text = text.replace('@HighlightColor', Style.colors.highlight)
        text = text.replace('@DarkTextColor', Style.colors.dark_text)
        text = text.replace('@LightTextColor', Style.colors.light_text)
        text = text.replace('@HeadTextSize', Style.text.head)
        text = text.replace('@SubTextSize', Style.text.subhead)
        text = text.replace('@ButtonTextSize', Style.text.button)
        text = text.replace('@LabelTextSize', Style.text.label)
        text = text.replace('@SmallTextSize', Style.text.small)
        text = text.replace('@LargeRadius', '30px')
        text = text.replace('@MediumRadius', '20px')
        text = text.replace('@SmallRadius', '15px')
        return text
