import os

from panda3d.core import PNMImage, SamplerState


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_TEXTURE_CACHE = {}


def _set_pixel(image, x, y, rgba):
    r, g, b, a = rgba
    image.set_xel(x, y, r / 255.0, g / 255.0, b / 255.0)
    image.set_alpha(x, y, a / 255.0)


def _build_meat_fish_texture(texture_path):
    image = PNMImage(16, 16, 4)
    for x in range(16):
        for y in range(16):
            image.set_xel(x, y, 0, 0, 0)
            image.set_alpha(x, y, 0)

    colors = {
        "outline": (50, 50, 50, 255),
        "body": (191, 201, 214, 255),
        "body2": (233, 242, 247, 255),
        "fin": (170, 186, 199, 255),
        "eye": (20, 20, 20, 255),
        "gill": (222, 150, 150, 255),
    }

    pixels = (
        (7, 2, "fin"), (8, 2, "fin"),
        (6, 3, "body"), (7, 3, "body"), (8, 3, "body2"), (9, 3, "body"), (10, 3, "fin"),
        (5, 4, "outline"), (6, 4, "body"), (7, 4, "body2"), (8, 4, "body2"), (9, 4, "body2"), (10, 4, "body"), (11, 4, "outline"),
        (4, 5, "outline"), (5, 5, "body"), (6, 5, "body2"), (7, 5, "body2"), (8, 5, "body2"), (9, 5, "body2"), (10, 5, "body2"), (11, 5, "body"), (12, 5, "outline"),
        (3, 6, "outline"), (4, 6, "body"), (5, 6, "body2"), (6, 6, "body2"), (7, 6, "body2"), (8, 6, "body2"), (9, 6, "body2"), (10, 6, "body2"), (11, 6, "body2"), (12, 6, "body"), (13, 6, "outline"),
        (2, 7, "outline"), (3, 7, "fin"), (4, 7, "body"), (5, 7, "body2"), (6, 7, "body2"), (7, 7, "body2"), (8, 7, "eye"), (9, 7, "body2"), (10, 7, "body2"), (11, 7, "gill"), (12, 7, "body"), (13, 7, "fin"), (14, 7, "outline"),
        (3, 8, "outline"), (4, 8, "body"), (5, 8, "body2"), (6, 8, "body2"), (7, 8, "body2"), (8, 8, "body2"), (9, 8, "body2"), (10, 8, "body2"), (11, 8, "body2"), (12, 8, "body"), (13, 8, "outline"),
        (4, 9, "outline"), (5, 9, "body"), (6, 9, "body2"), (7, 9, "body2"), (8, 9, "body2"), (9, 9, "body2"), (10, 9, "body2"), (11, 9, "body"), (12, 9, "outline"),
        (5, 10, "outline"), (6, 10, "body"), (7, 10, "body2"), (8, 10, "body2"), (9, 10, "body2"), (10, 10, "body"), (11, 10, "outline"),
        (6, 11, "fin"), (7, 11, "body"), (8, 11, "body2"), (9, 11, "body"), (10, 11, "fin"),
    )

    for x, y, color_name in pixels:
        _set_pixel(image, x, y, colors[color_name])

    image.write(texture_path)
    return os.path.exists(texture_path)


def get_texture_resource(texture_name):
    texture_path = os.path.join(BASE_DIR, "image", f"{texture_name}.png")
    if os.path.exists(texture_path):
        return f"image/{texture_name}.png"

    if texture_name == "meat_fish":
        if texture_name not in _TEXTURE_CACHE:
            _TEXTURE_CACHE[texture_name] = _build_meat_fish_texture(texture_path)
        if _TEXTURE_CACHE[texture_name]:
            return f"image/{texture_name}.png"

    return None


def apply_nearest_filter(texture):
    if texture is None:
        return

    # Ursina's loaded textures expose a `filtering` property, while our
    # runtime-generated fallback is a raw Panda3D Texture.
    try:
        texture.filtering = None
        return
    except Exception:
        pass

    if hasattr(texture, "set_magfilter"):
        texture.set_magfilter(SamplerState.FT_nearest)
    if hasattr(texture, "set_minfilter"):
        texture.set_minfilter(SamplerState.FT_nearest)
