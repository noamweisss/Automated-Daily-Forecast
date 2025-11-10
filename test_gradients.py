#!/usr/bin/env python3
"""
Test script for daily random gradient feature.

Tests gradient selection and image generation with mock data.
"""

from pathlib import Path
from datetime import datetime, timedelta
from generate_forecast_image import generate_all_cities_image

# Create mock forecast data for 15 cities
MOCK_CITIES = [
    {'name_eng': 'Qazrin', 'name_heb': 'קצרין', 'latitude': 33.0, 'min_temp': '15', 'max_temp': '25', 'weather_code': '1250'},
    {'name_eng': 'Zefat', 'name_heb': 'צפת', 'latitude': 32.96, 'min_temp': '14', 'max_temp': '24', 'weather_code': '1220'},
    {'name_eng': 'Bet Shean', 'name_heb': 'בית שאן', 'latitude': 32.5, 'min_temp': '18', 'max_temp': '30', 'weather_code': '1310'},
    {'name_eng': 'Tiberias', 'name_heb': 'טבריה', 'latitude': 32.79, 'min_temp': '17', 'max_temp': '28', 'weather_code': '1220'},
    {'name_eng': 'Haifa', 'name_heb': 'חיפה', 'latitude': 32.82, 'min_temp': '16', 'max_temp': '26', 'weather_code': '1250'},
    {'name_eng': 'Nazareth', 'name_heb': 'נצרת', 'latitude': 32.7, 'min_temp': '15', 'max_temp': '25', 'weather_code': '1230'},
    {'name_eng': 'Afula', 'name_heb': 'עפולה', 'latitude': 32.61, 'min_temp': '16', 'max_temp': '27', 'weather_code': '1220'},
    {'name_eng': 'Tel Aviv-Yafo', 'name_heb': 'תל אביב - יפו', 'latitude': 32.08, 'min_temp': '18', 'max_temp': '27', 'weather_code': '1250'},
    {'name_eng': 'Lod', 'name_heb': 'לוד', 'latitude': 31.95, 'min_temp': '17', 'max_temp': '28', 'weather_code': '1220'},
    {'name_eng': 'Ashdod', 'name_heb': 'אשדוד', 'latitude': 31.8, 'min_temp': '18', 'max_temp': '27', 'weather_code': '1250'},
    {'name_eng': 'Jerusalem', 'name_heb': 'ירושלים', 'latitude': 31.77, 'min_temp': '14', 'max_temp': '24', 'weather_code': '1250'},
    {'name_eng': 'En Gedi', 'name_heb': 'עין גדי', 'latitude': 31.46, 'min_temp': '20', 'max_temp': '32', 'weather_code': '1310'},
    {'name_eng': 'Beer Sheva', 'name_heb': 'באר שבע', 'latitude': 31.25, 'min_temp': '16', 'max_temp': '29', 'weather_code': '1250'},
    {'name_eng': 'Mizpe Ramon', 'name_heb': 'מצפה רמון', 'latitude': 30.61, 'min_temp': '12', 'max_temp': '26', 'weather_code': '1250'},
    {'name_eng': 'Elat', 'name_heb': 'אילת', 'latitude': 29.55, 'min_temp': '21', 'max_temp': '33', 'weather_code': '1310'},
]

def main():
    """Test gradient generation with multiple dates."""
    print("="*60)
    print("DAILY RANDOM GRADIENT TEST")
    print("="*60)

    # Ensure output directory exists
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    # Test with 3 different dates to see different gradients
    test_dates = [
        datetime.now().strftime('%Y-%m-%d'),
        (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
    ]

    print(f"\nTesting {len(test_dates)} different dates to verify gradient variety:")
    print()

    for date_str in test_dates:
        print(f"Testing date: {date_str}")
        output_path = output_dir / f"test_gradient_{date_str}.jpg"

        success = generate_all_cities_image(MOCK_CITIES, date_str, output_path)

        if success:
            print(f"  ✓ Successfully generated: {output_path}")
        else:
            print(f"  ✗ Failed to generate image for {date_str}")

        print()

    print("="*60)
    print("TEST COMPLETE")
    print("="*60)
    print("\nCheck the output/ directory for generated images:")
    print("  - test_gradient_<date>.jpg")
    print("\nEach image should have a different gradient background!")
    print("="*60)

if __name__ == "__main__":
    main()
