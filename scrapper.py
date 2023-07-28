import requests
import os
from bs4 import BeautifulSoup

# Create the directory if it doesn't exist
if not os.path.exists("scraped-html"):
    os.makedirs("scraped-html")

urls = {
    "news": "https://www.shegerfm.com",
    "today-news": "https://www.shegerfm.com/ወሬ/categories/የዛሬወሬ",
    "local-news": "https://www.shegerfm.com/ወሬ/categories/local-news",
    "international-news": "https://www.shegerfm.com/ወሬ/categories/international-news",
    "business-news": "https://www.shegerfm.com/ወሬ/categories/business-news",
    "economy": "https://www.shegerfm.com/ወሬ/categories/economy"
}


# A function to scrap the each page and save the html content to a file 
def scrapWebsite(url, fileName):
    try:
        # Open the URL and read the content
        content = requests.get(url).content

        # content = BeautifulSoup(content, 'html.parser')

        # Write the html content to a file
        with open(fileName, "w", encoding="utf-8") as file:
            file.write(content.decode("utf-8"))
    except Exception as e:
        print(f"Error occurred while scraping {url}: {e}")

# loop through the urls dictionary and call the scrapWebsite function
for key, value in urls.items():
    fileName = os.path.join("scraped-html", key + ".html")
    scrapWebsite(value, fileName)



