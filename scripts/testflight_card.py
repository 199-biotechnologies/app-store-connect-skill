#!/usr/bin/env python3
"""
TestFlight Invitation Card Generator

Generates a stylish, editorial-quality card with an artistic QR code
for sharing TestFlight beta links. Output is a high-res PNG.

Usage:
    python testflight_card.py <url> <app_name> [--subtitle "Join the beta"] [--style dark|light|electric|sunset] [--output card.png]

Examples:
    python testflight_card.py "https://testflight.apple.com/join/AbCdEf" "Simple Blood Pressure Log"
    python testflight_card.py "https://testflight.apple.com/join/AbCdEf" "Dream Journal" --style sunset
    python testflight_card.py "https://apps.apple.com/app/id123" "My App" --subtitle "Download now"

Requirements:
    pip install qrcode[pil] Pillow
"""

import argparse
import sys
from pathlib import Path

try:
    import qrcode
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer, CircleModuleDrawer
    from qrcode.image.styles.colormasks import RadialGradiantColorMask
except ImportError:
    # Older versions of qrcode have different import paths
    import qrcode
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, CircleModuleDrawer
    from qrcode.image.styles.colormasks import RadialGradiantColorMask

from PIL import Image, ImageDraw, ImageFont, ImageFilter


# ── Colour Palettes ──────────────────────────────────────────────────

STYLES = {
    "dark": {
        "bg": (15, 15, 20),
        "card_bg": (25, 25, 35),
        "accent": (99, 102, 241),       # Indigo
        "text": (255, 255, 255),
        "subtext": (160, 163, 175),
        "qr_center": (99, 102, 241),
        "qr_edge": (236, 72, 153),      # Pink
        "qr_bg": (255, 255, 255),
        "badge_bg": (99, 102, 241),
        "badge_text": (255, 255, 255),
    },
    "light": {
        "bg": (250, 250, 252),
        "card_bg": (255, 255, 255),
        "accent": (15, 15, 20),
        "text": (15, 15, 20),
        "subtext": (107, 114, 128),
        "qr_center": (15, 15, 20),
        "qr_edge": (75, 85, 99),
        "qr_bg": (255, 255, 255),
        "badge_bg": (15, 15, 20),
        "badge_text": (255, 255, 255),
    },
    "electric": {
        "bg": (0, 0, 0),
        "card_bg": (10, 10, 18),
        "accent": (0, 255, 136),         # Neon green
        "text": (255, 255, 255),
        "subtext": (0, 255, 136),
        "qr_center": (0, 255, 136),
        "qr_edge": (0, 180, 255),        # Cyan
        "qr_bg": (255, 255, 255),
        "badge_bg": (0, 255, 136),
        "badge_text": (0, 0, 0),
    },
    "sunset": {
        "bg": (30, 10, 40),
        "card_bg": (45, 15, 55),
        "accent": (255, 140, 50),        # Orange
        "text": (255, 255, 255),
        "subtext": (255, 180, 120),
        "qr_center": (255, 100, 50),
        "qr_edge": (200, 50, 180),       # Magenta
        "qr_bg": (255, 255, 255),
        "badge_bg": (255, 140, 50),
        "badge_text": (30, 10, 40),
    },
}


def get_font(size, bold=False):
    """Get the best available font."""
    font_paths = [
        # macOS system fonts
        "/System/Library/Fonts/SFProDisplay-Bold.otf" if bold else "/System/Library/Fonts/SFProDisplay-Regular.otf",
        "/System/Library/Fonts/SFProDisplay-Heavy.otf" if bold else "/System/Library/Fonts/SFProDisplay-Medium.otf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in font_paths:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def generate_qr(url, style, size=600):
    """Generate an artistic QR code with rounded dots and gradient."""
    palette = STYLES[style]

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High correction for style overlay
        box_size=12,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(radius_ratio=1.0),  # Fully rounded = dots
        color_mask=RadialGradiantColorMask(
            back_color=palette["qr_bg"],
            center_color=palette["qr_center"],
            edge_color=palette["qr_edge"],
        ),
    )

    # Convert and resize
    img = img.convert("RGBA")
    img = img.resize((size, size), Image.LANCZOS)
    return img


def draw_rounded_rect(draw, xy, radius, fill):
    """Draw a rounded rectangle."""
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill)


def generate_card(url, app_name, subtitle="Scan to join the beta", style="dark", output="testflight_card.png"):
    """Generate a complete TestFlight invitation card."""
    palette = STYLES[style]

    # Card dimensions (2:3 ratio, high-res)
    W, H = 1200, 1800
    MARGIN = 80
    CARD_RADIUS = 40

    # Create canvas
    canvas = Image.new("RGB", (W, H), palette["bg"])
    draw = ImageDraw.Draw(canvas)

    # ── Card background ──
    draw_rounded_rect(draw, (MARGIN, MARGIN, W - MARGIN, H - MARGIN), CARD_RADIUS, palette["card_bg"])

    # ── Accent line at top ──
    accent_y = MARGIN + 8
    draw_rounded_rect(
        draw,
        (MARGIN + 200, accent_y, W - MARGIN - 200, accent_y + 6),
        3,
        palette["accent"],
    )

    # ── Badge: "TestFlight" or "App Store" ──
    badge_font = get_font(28, bold=True)
    is_testflight = "testflight" in url.lower()
    badge_text = "TESTFLIGHT BETA" if is_testflight else "APP STORE"
    badge_y = MARGIN + 80

    bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
    badge_w = bbox[2] - bbox[0] + 48
    badge_h = bbox[3] - bbox[1] + 24
    badge_x = (W - badge_w) // 2

    draw_rounded_rect(
        draw,
        (badge_x, badge_y, badge_x + badge_w, badge_y + badge_h),
        badge_h // 2,
        palette["badge_bg"],
    )
    draw.text(
        (badge_x + 24, badge_y + 10),
        badge_text,
        fill=palette["badge_text"],
        font=badge_font,
    )

    # ── App name (large, bold, centered, multi-line if needed) ──
    title_font = get_font(72, bold=True)
    title_y = badge_y + badge_h + 60

    # Word-wrap the app name
    words = app_name.split()
    lines = []
    current_line = ""
    max_w = W - MARGIN * 2 - 80
    for word in words:
        test = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=title_font)
        if bbox[2] - bbox[0] <= max_w:
            current_line = test
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        lw = bbox[2] - bbox[0]
        draw.text(((W - lw) // 2, title_y), line, fill=palette["text"], font=title_font)
        title_y += bbox[3] - bbox[1] + 16

    # ── Subtitle ──
    sub_font = get_font(32, bold=False)
    sub_y = title_y + 20
    bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
    sw = bbox[2] - bbox[0]
    draw.text(((W - sw) // 2, sub_y), subtitle, fill=palette["subtext"], font=sub_font)

    # ── QR Code ──
    qr_size = 560
    qr_img = generate_qr(url, style, qr_size)

    # White rounded background for QR
    qr_bg_size = qr_size + 60
    qr_bg = Image.new("RGBA", (qr_bg_size, qr_bg_size), (0, 0, 0, 0))
    qr_bg_draw = ImageDraw.Draw(qr_bg)
    draw_rounded_rect(qr_bg_draw, (0, 0, qr_bg_size, qr_bg_size), 30, (255, 255, 255, 255))

    qr_total_y = sub_y + 80
    qr_bg_x = (W - qr_bg_size) // 2
    canvas.paste(Image.new("RGB", (qr_bg_size, qr_bg_size), (255, 255, 255)), (qr_bg_x, qr_total_y))

    # Paste QR on top
    qr_x = (W - qr_size) // 2
    qr_y = qr_total_y + 30
    canvas.paste(qr_img, (qr_x, qr_y), qr_img)

    # ── URL hint at bottom ──
    url_font = get_font(22, bold=False)
    # Show shortened URL
    display_url = url.replace("https://", "").replace("http://", "")
    if len(display_url) > 50:
        display_url = display_url[:47] + "..."

    url_y = qr_total_y + qr_bg_size + 40
    bbox = draw.textbbox((0, 0), display_url, font=url_font)
    uw = bbox[2] - bbox[0]
    draw.text(((W - uw) // 2, url_y), display_url, fill=palette["subtext"], font=url_font)

    # ── Bottom accent line ──
    bottom_y = H - MARGIN - 8
    draw_rounded_rect(
        draw,
        (MARGIN + 200, bottom_y - 6, W - MARGIN - 200, bottom_y),
        3,
        palette["accent"],
    )

    # ── Save ──
    canvas.save(output, "PNG", quality=95)
    print(f"Card saved: {output}")
    print(f"  Style: {style}")
    print(f"  Size: {W}x{H}")
    print(f"  App: {app_name}")
    print(f"  URL: {url}")
    return output


def main():
    parser = argparse.ArgumentParser(
        description="Generate a stylish TestFlight/App Store invitation card with artistic QR code"
    )
    parser.add_argument("url", help="TestFlight or App Store URL")
    parser.add_argument("app_name", help="App name to display on the card")
    parser.add_argument("--subtitle", default=None, help="Subtitle text (auto-detected if not set)")
    parser.add_argument("--style", choices=STYLES.keys(), default="dark", help="Visual style (default: dark)")
    parser.add_argument("--output", default=None, help="Output file path (default: <app_name>_card.png)")

    args = parser.parse_args()

    # Auto-detect subtitle
    if args.subtitle is None:
        if "testflight" in args.url.lower():
            args.subtitle = "Scan to join the beta"
        else:
            args.subtitle = "Scan to download"

    # Auto-generate output filename
    if args.output is None:
        safe_name = args.app_name.lower().replace(" ", "_")
        args.output = f"{safe_name}_card.png"

    generate_card(
        url=args.url,
        app_name=args.app_name,
        subtitle=args.subtitle,
        style=args.style,
        output=args.output,
    )


if __name__ == "__main__":
    main()
