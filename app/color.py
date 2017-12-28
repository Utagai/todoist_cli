import colored

GREEN = colored.fg('sea_green_3')
TURQ = colored.fg('pale_turquoise_4')
VIOLET = colored.fg('pale_violet_red_1')
BROWN = colored.fg('rosy_brown')
ORANGE = colored.fg('light_coral')
PURPLE = colored.fg('light_slate_grey')
BLUE = colored.fg('light_sky_blue_3a')
RED = colored.fg('deep_pink_2')

def _validate_prnt_args(*args):
    if len(args) % 2 != 0:
        err_msg = "There must be an even number of arguments to prnt()."
        raise ValueError(err_msg)

    args = list(args)

    msgs = args[:len(args)//2]
    colors = args[len(args)//2:]

    for color in colors:
        if color is None:
            continue
        color_isnt_str = not isinstance(color, str)
        is_not_ansi = '[' not in color
        valid_color = color_isnt_str or is_not_ansi
        if valid_color:
            err_msg = "The second half of arguments must be colors."
            raise ValueError(err_msg)

    return msgs, colors

def _nullify_nones(colors):
    for i in range(len(colors)):
        color = colors[i]
        if color is None:
            colors[i] = ""

    return colors

def prnt_str(*args):
    msgs, colors = _validate_prnt_args(*args)
    colors = _nullify_nones(colors)

    print_msg = ""
    for msg_color in zip(msgs, colors):
        print_msg += str(msg_color[1]) + str(msg_color[0])

    return print_msg

def prnt(*args):
    print(prnt_str(*args))
