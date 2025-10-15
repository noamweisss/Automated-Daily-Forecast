import xml.etree.ElementTree as ET

xml_file = r"C:\Users\noamw\Desktop\ims\Automated Daily Forecast\isr_cities_utf8.xml"

tree = ET.parse(xml_file)
root = tree.getroot()

# Get first location
first_location = root.find('.//Location')

print("="*60)
print("EXPLORING LocationData")
print("="*60 + "\n")

# Find the LocationData element
location_data = first_location.find('LocationData')

if location_data is not None:
    print(f"LocationData has {len(location_data)} children:\n")
    
    for child in location_data:
        print(f"<{child.tag}>: {child.text}")
        
        # If this child has children too, show them
        if len(child) > 0:
            print(f"  └─ (has {len(child)} sub-elements)")
            for subchild in child:
                text = subchild.text if subchild.text else "(empty)"
                print(f"     - <{subchild.tag}>: {text}")
        print()

print("="*60)