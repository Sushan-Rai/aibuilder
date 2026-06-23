from langchain.tools import tool
import requests
from bs4 import BeautifulSoup


@tool
def web_scrape(url: str):
    """
    Crawl a webpage URL and return cleaned text content.
    """
    print("SCRAPER CALLED:", url)
    try:

        headers = {
            "User-Agent":
            "Mozilla/5.0"
        }


        response = requests.get(
            url,
            headers=headers,
            timeout=15,
            allow_redirects=True
        )


        # size limit 1MB

        if len(response.content) > 1024*1024:

            return "Page too large"


        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


        # remove junk

        for tag in soup(
            [
                "script",
                "style",
                "noscript",
                "header",
                "footer"
            ]
        ):

            tag.decompose()



        text = soup.get_text(
            separator="\n"
        )


        cleaned = "\n".join(
            line.strip()
            for line in text.splitlines()
            if line.strip()
        )


        return cleaned[:5000]


    except Exception as e:

        return f"Scraping error: {str(e)}"