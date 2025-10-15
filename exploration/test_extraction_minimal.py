import xml.etree.ElementTree as ET

# Configuration
xml_file = r"C:\Users\noamw\Desktop\ims\Automated Daily Forecast\isr_cities_utf8.xml"
target_date = "2025-09-28"  # Use date that exists in XML

# Parse XML
print("Parsing XML file...")
tree = ET.parse(xml_file)
root = tree.getroot()

# Find Tel Aviv
print(f"Looking for Tel Aviv data on {target_date}...\n")
tel_aviv = None
for location in root.findall('.//Location'):
    name = location.find('.//LocationNameEng').text
    if name == "Tel Aviv - Yafo":
        tel_aviv = location
        break

if tel_aviv is None:
    print("ERROR: Tel Aviv not found!")
    exit()

# Extract metadata
metadata = tel_aviv.find('LocationMetaData')
city_name_eng = metadata.find('LocationNameEng').text
city_name_heb = metadata.find('LocationNameHeb').text
latitude = metadata.find('DisplayLat').text
longitude = metadata.find('DisplayLon').text

print("="*50)
print(f"CITY: {city_name_eng}")
print(f"Hebrew: {city_name_heb}")
print(f"Coordinates: {latitude}°N, {longitude}°E")
print("="*50)

# Find the forecast for target date
location_data = tel_aviv.find('LocationData')
target_forecast = None

for time_unit in location_data.findall('TimeUnitData'):
    date = time_unit.find('Date').text
    if date == target_date:
        target_forecast = time_unit
        break

if target_forecast is None:
    print(f"ERROR: No forecast found for {target_date}")
    exit()

print(f"\nForecast for: {target_date}\n")

# Extract weather data
max_temp = None
min_temp = None
weather_code = None

for element in target_forecast.findall('Element'):
    elem_name = element.find('ElementName').text
    elem_value = element.find('ElementValue').text

    if elem_name == "Maximum temperature":
        max_temp = elem_value
    elif elem_name == "Minimum temperature":
        min_temp = elem_value
    elif elem_name == "Weather code":
        weather_code = elem_value

# Display results
print(f"Maximum Temperature: {max_temp}°C")
print(f"Minimum Temperature: {min_temp}°C")
print(f"Weather Code: {weather_code}")
print("\n" + "="*50)
print("SUCCESS! Basic extraction works!")
print("="*50)
