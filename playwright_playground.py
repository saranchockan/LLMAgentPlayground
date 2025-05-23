from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def extract_all_text(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        # Get the full HTML content
        html_content = page.content()

        # Parse HTML and extract text
        soup = BeautifulSoup(html_content, "html.parser")
        all_text = soup.get_text(separator=" ", strip=True)

        browser.close()
        return all_text


def get_element_raw_html_text(url: str, selector: str):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        elements = page.query_selector_all(selector=selector)

        for element in elements:
            print(element.evaluate("el => el.outerHTML"))

        browser.close()


url = "https://boards.greenhouse.io/anthropic/jobs/4020295008"
print(
    extract_all_text(
        url=url,
    )
)
