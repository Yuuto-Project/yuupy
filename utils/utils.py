def color_hex_to_0x(hexstr):
    return '0x' + hexstr.replace('#', '')


def color_hex_to_int(hexstr):
    return int(color_hex_to_0x(hexstr), 16)
