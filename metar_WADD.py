import requests
import xml.etree.ElementTree as ET
import datetime

# Function to create pubDate for RSS
def format_pubdate():
    return datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S %z')

# Fetch the data from the URL
url = 'https://aviationweather.gov/api/data/metar?ids=WADD'
response = requests.get(url)

# Check if the response is valid
if response.status_code == 200 and 'text/plain' in response.headers.get('Content-Type', ''):
    metar_data = response.text.strip()
else:
    print(f"Error: Failed to fetch data or the response is not plain text. Status code: {response.status_code}")
    metar_data = None

if metar_data:
    # Get the current time in a readable format for the title
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create the root element
    rss = ET.Element('rss')
    rss.set('version', '2.0')

    # Create the channel element
    channel = ET.SubElement(rss, 'channel')

    # Add channel elements
    title = ET.SubElement(channel, 'title')
    title.text = 'Aviation Weather METAR Data for WADD'

    link = ET.SubElement(channel, 'link')
    link.text = url

    description = ET.SubElement(channel, 'description')
    description.text = 'Latest METAR data for WADD'

    # Add an item for the METAR report
    item = ET.SubElement(channel, 'item')

    # Update item title with the current time of the update
    item_title = ET.SubElement(item, 'title')
    item_title.text = f"METAR Report Update at {current_time}"

    item_link = ET.SubElement(item, 'link')
    item_link.text = url

    item_description = ET.SubElement(item, 'description')
    item_description.text = metar_data

    item_pubDate = ET.SubElement(item, 'pubDate')
    item_pubDate.text = format_pubdate()

    # Convert the ElementTree to a string
    rss_feed = ET.tostring(rss, encoding='unicode', method='xml')

    # Save to a file
    with open('wadd_metar_rss_feed.xml', 'w') as file:
        file.write(rss_feed)

    print('RSS feed generated and saved as wadd_metar_rss_feed.xml')
else:
    print("Failed to generate RSS feed due to invalid data.")
