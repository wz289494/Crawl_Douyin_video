# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# Useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import requests

class DouyinVideoPipeline:
    def process_item(self, item, spider):
        """
        Process each item by downloading the video and saving it to a file.

        Parameters:
        item (dict): The item containing video information.
        spider (scrapy.Spider): The spider that scraped the item.

        Returns:
        dict: The processed item.
        """
        if 'video_url' in item and 'video_title' in item:
            video_url = item['video_url']
            video_title = item['video_title']
            # Ensure the video URL starts with 'http:' or 'https:'
            if not video_url.startswith(('http:', 'https:')):
                video_url = 'https:' + video_url

            # Create a valid filename by removing invalid characters
            filename = "".join([c for c in video_title if c.isalpha() or c.isdigit() or c == ' ']).rstrip()
            file_path = os.path.join('..\\爬取视频', f"{item['video_id']}-{filename}.mp4")

            response = requests.get(video_url, stream=True)
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                spider.logger.info(f'Video saved as {file_path}')
            else:
                spider.logger.warning(f'Failed to save video: {video_url}')

        return item
