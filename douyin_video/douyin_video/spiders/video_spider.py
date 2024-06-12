import time
import re
import scrapy
import pandas as pd
from douyin_video.items import DouyinVideoItem


class VideoSpiderSpider(scrapy.Spider):
    name = "video_spider"
    # Path to the Excel file containing URLs
    excel_path = '..\\网址目录\\list_all.xlsx'
    # Column in the Excel file that contains the URLs
    url_column = '完整视频链接'

    def start_requests(self):
        """
        Start requests by reading URLs from the specified Excel file and initiating requests.
        """
        # Read the Excel file using pandas
        df = pd.read_excel(self.excel_path, engine='openpyxl')
        # Iterate over the specified column to get all URLs
        for url in df[self.url_column].dropna():
            # Extract video ID from the URL
            video_id = self.extract_video_id(url)
            # Print the URL for debugging purposes
            print(url)
            # Sleep for 1 second to avoid being blocked
            time.sleep(1)
            # Make a request to each URL and pass the video ID as a meta parameter
            yield scrapy.Request(url=url, callback=self.parse, meta={'video_id': video_id})

    def parse(self, response):
        """
        Parse the response to extract video information.

        Parameters:
        response (scrapy.http.Response): The response object containing the HTML content.

        Returns:
        DouyinVideoItem: The item containing extracted video information.
        """
        # Get the video ID passed as a meta parameter
        video_id = response.meta.get('video_id')
        # Locate all <source> tags to get the video URL
        source_elements = response.xpath("//xg-video-container/video/source/@src")

        # Locate the video title using XPath
        title_element = response.xpath(
            "//*[@id='douyin-right-container']/div[2]/div/div[1]/div[3]/div/div[1]/div/h1/span/span[2]/span/span/span/span/span/text()").get()

        # Extract the first video URL from the <source> elements
        video_url = source_elements.getall()[0]
        # Strip whitespace from the title
        video_title = title_element.strip()

        # Create an item container for the video information
        item = DouyinVideoItem()

        item['video_url'] = video_url
        item['video_title'] = video_title
        item['video_id'] = video_id

        # Print the item for debugging purposes
        print(item)

        # Yield the item to be processed by the pipeline
        yield item

    def extract_video_id(self, url):
        """
        Extract the video ID from a given URL.

        Parameters:
        url (str): The URL of the video.

        Returns:
        str: The extracted video ID or None if no ID is found.
        """
        # Use a regular expression to match the video ID
        match = re.search(r'video/(\d+)', url)
        if match:
            return match.group(1)
        else:
            return None
