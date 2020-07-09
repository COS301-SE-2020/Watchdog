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
    sizes.margin_large = 35
    # Margin
    sizes.margin_medium = 15
    # Margin
    sizes.margin_small = 5
    # Padding
    sizes.padding_large = 15
    # Padding
    sizes.padding_medium = 10
    # Padding
    sizes.padding_small = 2

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

        Style.sizes.radius_large = int(Style.unit / 12.8)  # 30px
        Style.sizes.radius_medium = int(Style.unit / 19.2)  # 20px
        Style.sizes.radius_small = int(Style.unit / 25.6)  # 15px
        Style.sizes.icon_logo = int(Style.unit * 0.33)
        Style.sizes.icon_large = int(Style.unit / 4)
        Style.sizes.icon_medium = int(Style.unit / 8)
        Style.sizes.icon_small = int(Style.unit / 15)

        Style.sizes.border_thick = int(Style.unit / 192)  # 2
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
        text = text.replace('@LightColor', Style.colors.light)
        text = text.replace('@HighlightColor', Style.colors.highlight)
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
