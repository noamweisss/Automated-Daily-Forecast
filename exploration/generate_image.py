"""
IMS Weather Forecast Automation - Phase 2: Image Generation POC

Single city image generation proof-of-concept with Hebrew RTL text support.
Generates a simple Instagram story image (1080x1920px) for one city.
"""

import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from bidi.algorithm import get_display

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from extract_forecast import extract_forecast


# ============================================================================
# CONFIGURATION
# ============================================================================

# Image dimensions (Instagram story format)
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1920

# Output directory
OUTPUT_DIR = Path(__file__).parent.parent / "output"

# Font paths
FONT_DIR = Path(__file__).parent.parent / "fonts"
FONT_VARIABLE = FONT_DIR / "Heebo-Variable.ttf"

# Colors (RGB)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (100, 100, 100)
COLOR_SKY_LIGHT = (135, 206, 250)  # Light sky blue
COLOR_SKY_MEDIUM = (100, 180, 255)  # Medium sky blue


# ============================================================================
# WEATHER CODE MAPPING
# ============================================================================

WEATHER_EMOJI = {
    '1250': '☀️',      # Clear/Sunny
    '1220': '⛅',      # Partly Cloudy
    '1310': '🌤️',     # Mostly Clear
    '1580': '🌡️☀️',   # Very Hot/Sunny
    # Add more codes as needed
}


def get_weather_emoji(weather_code: str) -> str:
    """
    Get emoji for weather code, with fallback.

    Args:
        weather_code: Weather code from XML

    Returns:
        Weather emoji string
    """
    return WEATHER_EMOJI.get(weather_code, '🌤️')  # Default to mostly clear


# ============================================================================
# IMAGE GENERATION FUNCTIONS
# ============================================================================

def create_gradient_background(width: int, height: int) -> Image.Image:
    """
    Create a simple vertical gradient background.

    Args:
        width: Image width in pixels
        height: Image height in pixels

    Returns:
        PIL Image with gradient background
    """
    # Create blank image
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)

    # Draw vertical gradient from top (light blue) to bottom (white)
    for y in range(height):
        # Calculate color interpolation
        ratio = y / height
        r = int(COLOR_SKY_LIGHT[0] + (COLOR_WHITE[0] - COLOR_SKY_LIGHT[0]) * ratio)
        g = int(COLOR_SKY_LIGHT[1] + (COLOR_WHITE[1] - COLOR_SKY_LIGHT[1]) * ratio)
        b = int(COLOR_SKY_LIGHT[2] + (COLOR_WHITE[2] - COLOR_SKY_LIGHT[2]) * ratio)

        draw.line([(0, y), (width, y)], fill=(r, g, b))

    return image


def render_hebrew_text(text: str) -> str:
    """
    Convert Hebrew text to proper RTL display format.

    Args:
        text: Hebrew text string

    Returns:
        RTL-formatted text ready for rendering
    """
    return get_display(text)


def generate_city_image(city_data: dict, output_path: Path) -> bool:
    """
    Generate a weather forecast image for one city.

    Args:
        city_data: Dictionary with city forecast data
        output_path: Path to save the image

    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"\nGenerating image for: {city_data['name_eng']}")

        # Create canvas with gradient background
        print("Creating canvas with gradient background...")
        image = create_gradient_background(IMAGE_WIDTH, IMAGE_HEIGHT)
        draw = ImageDraw.Draw(image)

        # Load fonts (using variable font)
        print("Loading fonts...")
        font_city_name = ImageFont.truetype(str(FONT_VARIABLE), 120)
        font_temp = ImageFont.truetype(str(FONT_VARIABLE), 100)
        font_emoji = ImageFont.truetype(str(FONT_VARIABLE), 150)

        # Prepare text content
        city_name_heb = city_data['name_heb']
        city_name_display = render_hebrew_text(city_name_heb)

        temp_min = city_data['min_temp']
        temp_max = city_data['max_temp']
        temp_text = f"{temp_min}-{temp_max}°C"

        weather_code = city_data['weather_code']
        weather_emoji = get_weather_emoji(weather_code)

        print(f"  Temperature: {temp_text}")
        print(f"  Weather Code: {weather_code}")
        # Note: Not printing Hebrew text or emojis due to Windows console encoding

        # Calculate vertical positions (centered vertically)
        center_y = IMAGE_HEIGHT // 2

        # Position 1: Weather emoji at top-center
        emoji_y = center_y - 300

        # Get emoji text dimensions for centering
        emoji_bbox = draw.textbbox((0, 0), weather_emoji, font=font_emoji)
        emoji_width = emoji_bbox[2] - emoji_bbox[0]
        emoji_x = (IMAGE_WIDTH - emoji_width) // 2

        # Draw weather emoji
        # Note: Emojis might not render with all fonts, so we draw as text
        draw.text((emoji_x, emoji_y), weather_emoji, fill=COLOR_BLACK, font=font_emoji, embedded_color=True)

        # Position 2: City name below emoji
        city_y = emoji_y + 200

        # Get city name dimensions for centering
        city_bbox = draw.textbbox((0, 0), city_name_display, font=font_city_name)
        city_width = city_bbox[2] - city_bbox[0]
        city_x = (IMAGE_WIDTH - city_width) // 2

        # Draw city name (Hebrew RTL)
        draw.text((city_x, city_y), city_name_display, fill=COLOR_BLACK, font=font_city_name)

        # Position 3: Temperature below city name
        temp_y = city_y + 150

        # Get temperature dimensions for centering
        temp_bbox = draw.textbbox((0, 0), temp_text, font=font_temp)
        temp_width = temp_bbox[2] - temp_bbox[0]
        temp_x = (IMAGE_WIDTH - temp_width) // 2

        # Draw temperature
        draw.text((temp_x, temp_y), temp_text, fill=COLOR_GRAY, font=font_temp)

        # Save image
        print(f"Saving image to: {output_path}")
        image.save(output_path, 'JPEG', quality=95)
        print("OK Image saved successfully!")

        return True

    except Exception as e:
        print(f"X Error generating image: {e}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================================
# MAIN SCRIPT
# ============================================================================

def main():
    """Main entry point for the script."""
    print("="*60)
    print("IMS WEATHER FORECAST - IMAGE GENERATION POC")
    print("="*60)

    # Extract forecast data
    print("\nExtracting forecast data...")
    cities_data = extract_forecast()

    if not cities_data:
        print("X Failed to extract forecast data")
        sys.exit(1)

    # Find Tel Aviv (our test city)
    tel_aviv = None
    for city in cities_data:
        if city['name_eng'] == 'Tel Aviv - Yafo':
            tel_aviv = city
            break

    if not tel_aviv:
        print("X Tel Aviv not found in forecast data")
        sys.exit(1)

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Generate image
    output_path = OUTPUT_DIR / "test_city_forecast.jpg"
    success = generate_city_image(tel_aviv, output_path)

    # Summary
    print("\n" + "="*60)
    if success:
        print("SUCCESS! Image generation complete!")
        print(f"Output: {output_path}")
        print("\nNext steps:")
        print("1. Open the image to verify Hebrew text displays correctly")
        print("2. Check that temperature and emoji are visible")
        print("3. Iterate on design/layout if needed")
    else:
        print("FAILED! Check error messages above")
    print("="*60)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
