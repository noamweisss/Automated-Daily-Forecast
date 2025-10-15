import xml.etree.ElementTree as ET

# Configuration
xml_file = r"C:\Users\noamw\Desktop\ims\Automated Daily Forecast\isr_cities_utf8.xml"
target_date = "2025-09-28"  # Use date that exists in XML

# Parse XML
print("="*60)
print("IMS WEATHER FORECAST EXTRACTOR")
print("="*60)
print(f"\nParsing XML file...")
tree = ET.parse(xml_file)
root = tree.getroot()

# Get issue date
issue_date = root.find('.//IssueDateTime').text
print(f"Forecast issued: {issue_date}")
print(f"Extracting data for: {target_date}\n")

# Storage for extracted data
cities_data = []

# Loop through all locations
locations = root.findall('.//Location')
print(f"Found {len(locations)} cities in XML file\n")
print("Extracting forecast data...")
print("-"*60)

for location in locations:
    # Extract metadata
    metadata = location.find('LocationMetaData')
    city_name_eng = metadata.find('LocationNameEng').text
    city_name_heb = metadata.find('LocationNameHeb').text
    latitude = float(metadata.find('DisplayLat').text)
    longitude = float(metadata.find('DisplayLon').text)

    # Find the forecast for target date
    location_data = location.find('LocationData')
    target_forecast = None

    for time_unit in location_data.findall('TimeUnitData'):
        date = time_unit.find('Date').text
        if date == target_date:
            target_forecast = time_unit
            break

    # If no forecast found for this date, skip this city
    if target_forecast is None:
        print(f"WARNING: No forecast for {city_name_eng} on {target_date}")
        continue

    # Extract weather data
    max_temp = None
    min_temp = None
    weather_code = None
    max_humidity = None
    min_humidity = None
    wind = None

    for element in target_forecast.findall('Element'):
        elem_name = element.find('ElementName').text
        elem_value = element.find('ElementValue').text

        if elem_name == "Maximum temperature":
            max_temp = elem_value
        elif elem_name == "Minimum temperature":
            min_temp = elem_value
        elif elem_name == "Weather code":
            weather_code = elem_value
        elif elem_name == "Maximum relative humidity":
            max_humidity = elem_value
        elif elem_name == "Minimum relative humidity":
            min_humidity = elem_value
        elif elem_name == "Wind direction and speed":
            wind = elem_value

    # Store the city data
    city_info = {
        'name_eng': city_name_eng,
        'name_heb': city_name_heb,
        'latitude': latitude,
        'longitude': longitude,
        'max_temp': max_temp,
        'min_temp': min_temp,
        'weather_code': weather_code,
        'max_humidity': max_humidity,
        'min_humidity': min_humidity,
        'wind': wind
    }

    cities_data.append(city_info)
    print(f"  {city_name_eng:20s} | Lat: {latitude:6.2f}N | Temp: {min_temp}-{max_temp}C | Code: {weather_code}")

# Sort cities by latitude (north to south = highest to lowest)
cities_data.sort(key=lambda city: city['latitude'], reverse=True)

# Display sorted results
print("\n" + "="*60)
print("CITIES SORTED BY LATITUDE (NORTH TO SOUTH)")
print("="*60)
print(f"\nTotal cities extracted: {len(cities_data)}\n")

for i, city in enumerate(cities_data, 1):
    print(f"{i:2d}. {city['name_eng']:20s} ({city['latitude']:6.2f}N) | {city['min_temp']}-{city['max_temp']}C | Code: {city['weather_code']}")

# Display detailed data for verification
print("\n" + "="*60)
print("DETAILED FORECAST DATA")
print("="*60)

for city in cities_data:
    print(f"\n{city['name_eng']} (Hebrew: {city['name_heb']})")
    print(f"  Location: {city['latitude']}N, {city['longitude']}E")
    print(f"  Temperature: {city['min_temp']}C - {city['max_temp']}C")
    print(f"  Weather Code: {city['weather_code']}")
    if city['max_humidity']:
        print(f"  Humidity: {city['min_humidity']}-{city['max_humidity']}%")
    if city['wind']:
        print(f"  Wind: {city['wind']}")

# Summary
print("\n" + "="*60)
print("EXTRACTION COMPLETE!")
print("="*60)
print(f"Successfully extracted {len(cities_data)} cities")
print(f"Date: {target_date}")
print(f"Sorted: North to South by latitude")
print("="*60)
