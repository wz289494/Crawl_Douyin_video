import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from scrapy.http import HtmlResponse

class VideoloadMiddleware:
    def __init__(self):
        """
        Initialize the middleware by setting up the Chrome WebDriver in headless mode.
        """
        # Configure ChromeOptions to enable headless mode
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Add headless argument
        # Create a driver object
        self.driver = webdriver.Chrome(options=chrome_options)

    def process_request(self, request, spider):
        """
        Process the request using Selenium WebDriver.

        Parameters:
        request (scrapy.Request): The Scrapy request object.
        spider (scrapy.Spider): The Scrapy spider object.

        Returns:
        HtmlResponse: The response object containing the page source.
        """
        # Open the URL
        self.driver.get(request.url)
        # Log in using cookies
        self.log_cookie()
        # Wait for the specific element to appear on the page
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//*[@id='douyin-right-container']/div[2]/div/div[1]/div[2]/div/xg-video-container/video/source[3]"))
            )
            page_source = self.driver.page_source
            return HtmlResponse(url=request.url, body=page_source, request=request, encoding='utf-8')
        except Exception as e:
            spider.logger.error(f"Error while waiting for element: {e}")
            return HtmlResponse(url=request.url, status=500, request=request)

    def log_cookie(self):
        """
        Log in to the browser by adding cookies from a file.

        Returns:
        None
        """
        # Read cookie login file
        with open(r'..\config_cookies.txt', 'r', encoding='utf8') as f:
            listCookies = json.loads(f.read())

        # Add cookies to the browser
        for cookie in listCookies:
            cookie_dict = {
                'domain': '.douyin.com',
                'name': cookie.get('name'),
                'value': cookie.get('value'),
                "expires": cookie.get('expiry'),
                'path': '/',
                'httpOnly': False,
                'HostOnly': False,
                'Secure': False
            }

            self.driver.add_cookie(cookie_dict)

        # Refresh the page for cookies to take effect
        self.driver.refresh()
