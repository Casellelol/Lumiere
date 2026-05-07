"""
Lumière Prints — Design Generator
Generates high-res wall art prints (3000x4000px, 300 DPI) for Etsy digital download.
Styles: minimalist quotes, abstract, botanical, geometric
"""

from PIL import Image, ImageDraw, ImageFont
import os, json, random

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Canvas sizes (300 DPI)
SIZES = {
    "8x10":  (2400, 3000),
    "11x14": (3300, 4200),
    "16x20": (4800, 6000),
}
PRIMARY_SIZE = "8x10"
W, H = SIZES[PRIMARY_SIZE]

# Palettes
PALETTES = {
    "ivory-gold": {
        "bg": (250, 248, 244),
        "primary": (30, 28, 26),
        "accent": (180, 148, 90),
        "secondary": (140, 132, 120),
    },
    "sage-linen": {
        "bg": (232, 236, 228),
        "primary": (45, 55, 40),
        "accent": (120, 140, 100),
        "secondary": (100, 110, 90),
    },
    "midnight-cream": {
        "bg": (18, 18, 22),
        "primary": (240, 238, 232),
        "accent": (180, 148, 90),
        "secondary": (140, 136, 128),
    },
    "dusty-rose-white": {
        "bg": (248, 240, 240),
        "primary": (80, 50, 55),
        "accent": (180, 120, 120),
        "secondary": (160, 130, 130),
    },
    "navy-gold": {
        "bg": (22, 30, 50),
        "primary": (235, 230, 218),
        "accent": (180, 148, 90),
        "secondary": (120, 130, 155),
    },
}

QUOTES = [
    ("Be still.", "find peace in the quiet"),
    ("Slow down.", "life is not a race"),
    ("You are enough.", "always, in every season"),
    ("Breathe.", "this too shall pass"),
    ("Less, but better.", "the quiet luxury of restraint"),
    ("Create space.", "for what matters most"),
    ("Stay soft.", "in a world that pulls you hard"),
    ("Begin again.", "every morning is a new start"),
    ("Presence\nis a gift.", "give it freely"),
    ("Do less.\nBe more.", "the art of subtraction"),
    ("Quiet\nconfidence.", "needs no announcement"),
    ("Tend to\nyourself.", "as you would a garden"),
    ("Choose calm.", "it is always an option"),
    ("You belong\nhere.", "fully and completely"),
    ("Rest is\nproductive.", "allow yourself to pause"),
]

def make_quote_print(quote_main, quote_sub, palette_name, design_id):
    p = PALETTES[palette_name]
    img = Image.new("RGB", (W, H), p["bg"])
    draw = ImageDraw.Draw(img)

    font_large = ImageFont.load_default(size=int(W * 0.072))
    font_small  = ImageFont.load_default(size=int(W * 0.028))
    font_brand  = ImageFont.load_default(size=int(W * 0.022))

    # Top rule line
    line_y = int(H * 0.12)
    draw.line([(int(W*0.35), line_y), (int(W*0.65), line_y)], fill=p["accent"], width=2)

    # Main quote
    draw.text((W//2, H//2 - int(H*0.06)), quote_main,
              fill=p["primary"], anchor="mm", font=font_large, align="center")

    # Sub quote
    draw.text((W//2, H//2 + int(H*0.10)), quote_sub,
              fill=p["secondary"], anchor="mm", font=font_small, align="center")

    # Bottom rule + brand
    bot_y = int(H * 0.88)
    draw.line([(int(W*0.35), bot_y), (int(W*0.65), bot_y)], fill=p["accent"], width=2)
    draw.text((W//2, int(H*0.92)), "LUMIÈRE",
              fill=p["accent"], anchor="mm", font=font_brand)

    path = os.path.join(OUTPUT_DIR, f"{design_id}.jpg")
    img.save(path, "JPEG", quality=95, dpi=(300, 300))
    return path


def make_abstract_print(palette_name, design_id):
    p = PALETTES[palette_name]
    img = Image.new("RGB", (W, H), p["bg"])
    draw = ImageDraw.Draw(img)

    # Minimalist abstract: a few geometric shapes
    cx, cy = W // 2, H // 2

    # Large circle outline
    r = int(W * 0.28)
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=p["accent"], width=3)

    # Offset smaller circle
    r2 = int(W * 0.16)
    draw.ellipse([cx-r2+int(W*0.08), cy-r2-int(H*0.06),
                  cx+r2+int(W*0.08), cy+r2-int(H*0.06)], outline=p["primary"], width=2)

    # Horizontal lines at top and bottom
    for i in range(3):
        y = int(H * 0.15) + i * int(H * 0.018)
        draw.line([(int(W*0.3), y), (int(W*0.7), y)], fill=p["secondary"], width=1)
        y2 = int(H * 0.82) + i * int(H * 0.018)
        draw.line([(int(W*0.3), y2), (int(W*0.7), y2)], fill=p["secondary"], width=1)

    # Brand
    font_brand = ImageFont.load_default(size=int(W * 0.022))
    draw.text((W//2, int(H*0.92)), "LUMIÈRE",
              fill=p["accent"], anchor="mm", font=font_brand)

    path = os.path.join(OUTPUT_DIR, f"{design_id}.jpg")
    img.save(path, "JPEG", quality=95, dpi=(300, 300))
    return path


def generate_all():
    designs = []

    # Quote prints — all palette × quote combinations
    for i, (quote_main, quote_sub) in enumerate(QUOTES):
        for palette_name in PALETTES:
            design_id = f"quote-{i:02d}-{palette_name}"
            path = make_quote_print(quote_main, quote_sub, palette_name, design_id)
            designs.append({
                "id": design_id,
                "type": "quote",
                "quote": quote_main,
                "palette": palette_name,
                "path": path,
            })
            print(f"  ✓ {design_id}")

    # Abstract prints — one per palette
    for palette_name in PALETTES:
        design_id = f"abstract-{palette_name}"
        path = make_abstract_print(palette_name, design_id)
        designs.append({
            "id": design_id,
            "type": "abstract",
            "palette": palette_name,
            "path": path,
        })
        print(f"  ✓ {design_id}")

    # Save manifest
    manifest_path = os.path.join(OUTPUT_DIR, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(designs, f, indent=2)

    print(f"\n✅ Generated {len(designs)} designs → {OUTPUT_DIR}")
    return designs


if __name__ == "__main__":
    print("Lumière — Generating designs...\n")
    generate_all()
