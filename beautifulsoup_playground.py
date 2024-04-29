import requests
from bs4 import BeautifulSoup

# Fetch the main page
main_url = "http://www.therentalshow.com/find-exhibitors/sb-search/equipment/sb-inst/8678/sb-logid/242109-dcja1tszmylg308y/sb-page/1"
response = requests.get(main_url)
soup = BeautifulSoup(response.content, "html.parser")

# Extract URLs from the main page
main_page_urls = []
for link in soup.find_all("a", {"class": "avtsb_title"}):
    main_page_urls.append("http://www.therentalshow.com" + link.get("href"))

# Extract URLs from the nested pages
all_urls = main_page_urls.copy()
for nested_url in main_page_urls:
    nested_response = requests.get(nested_url)
    nested_soup = BeautifulSoup(nested_response.content, "html.parser")
    for link in nested_soup.find_all("a"):
        all_urls.append(link.get("href"))

# Print all the URLs
for url in all_urls:
    print(url)
