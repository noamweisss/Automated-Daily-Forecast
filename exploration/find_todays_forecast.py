import xml.etree.ElementTree as ET
from datetime import date

xml_file = r"C:\Users\noamw\Desktop\ims\Automated Daily Forecast\isr_cities_utf8.xml"

# Parse XML
tree = ET.parse(xml_file)
root = tree.getroot()

# Get today's date
today = str(date.today())
print(f"Today is: {today}\n")

# Get first location (just for testing)
first_location = root.find('.//Location')
location_data = first_location.find('LocationData')

# Loop through all TimeUnitData elements for the first location and print their dates
for time_unit in location_data.findall('TimeUnitData'):
    date_elem = time_unit.find('Date')
    date_str = getattr(date_elem, "text", None)
    print(f"TimeUnitData Date: {date_str}")