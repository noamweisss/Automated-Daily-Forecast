import xml.etree.ElementTree as ET

xml_file = r"C:\Users\noamw\Desktop\ims\Automated Daily Forecast\isr_cities_utf8.xml"

tree = ET.parse(xml_file)
root = tree.getroot()

# Get first location
first_location = root.find('.//Location')
location_data = first_location.find('LocationData')

print("="*60)
print("DEEP DIVE INTO ELEMENTS")
print("="*60 + "\n")

# Get the first TimeUnitData (first forecast day)
first_day = location_data.find('TimeUnitData')
date = first_day.find('Date').text
print(f"Looking at forecast for: {date}\n")

# Get all Element children
elements = first_day.findall('Element')
print(f"Found {len(elements)} <Element> tags\n")

# Examine each Element in detail
for i, element in enumerate(elements, 1):
    print(f"Element #{i}:")
    print(f"  Attributes: {element.attrib}")  # This shows attributes!
    print(f"  Direct text: '{element.text}'")
    print(f"  Number of children: {len(element)}")
    
    # Show what's inside
    if len(element) > 0:
        print(f"  Children inside:")
        for child in element:
            print(f"    - <{child.tag}>: {child.text}")
    
    print()