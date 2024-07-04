# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: URL Crawler Tool
"""
import hashlib
import json
import os
import re
from urllib.parse import urlparse

import markdownify
import requests
from bs4 import BeautifulSoup

from agentica.tool import Toolkit
from agentica.utils.log import logger


class UrlCrawlerTool(Toolkit):
    work_dir: str = os.path.curdir

    def __init__(self, work_dir: str = None):
        super().__init__(name="url_crawler_tool")
        self.work_dir = work_dir if work_dir is not None else self.work_dir
        self.register(self.url_crawl)

    @staticmethod
    def _generate_file_name_from_url(url: str, max_length=255) -> str:
        url_bytes = url.encode("utf-8")
        hash = hashlib.blake2b(url_bytes).hexdigest()
        parsed_url = urlparse(url)
        file_name = os.path.basename(url)
        file_name = f"{parsed_url.netloc}_{file_name}_{hash[:min(8, max_length - len(parsed_url.netloc) - len(file_name) - 1)]}"
        return file_name

    @staticmethod
    def parse_html_to_markdown(html: str, url: str = None) -> str:
        """Parse HTML to markdown."""
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string
        # Remove javascript and style blocks
        for script in soup(["script", "style"]):
            script.extract()

        # Convert to markdown -- Wikipedia gets special attention to get a clean version of the page
        if isinstance(url, str) and "wikipedia.org" in url:
            body_elm = soup.find("div", {"id": "mw-content-text"})
            title_elm = soup.find("span", {"class": "mw-page-title-main"})

            if body_elm:
                # What's the title
                main_title = soup.title.string
                if title_elm and len(title_elm) > 0:
                    main_title = title_elm.string
                webpage_text = "# " + main_title + "\n\n" + markdownify.MarkdownConverter().convert_soup(body_elm)
            else:
                webpage_text = markdownify.MarkdownConverter().convert_soup(soup)
        else:
            webpage_text = markdownify.MarkdownConverter().convert_soup(soup)

        # Convert newlines
        webpage_text = re.sub(r"\r\n", "\n", webpage_text)
        webpage_text = re.sub(r"\n{2,}", "\n\n", webpage_text).strip()
        webpage_text = "# " + title + "\n\n" + webpage_text
        return webpage_text

    def crawl_url_to_file(self, url: str):
        """
        Crawls a website and saves the content to a file.
        """
        filename = self._generate_file_name_from_url(url)
        save_path = os.path.realpath(os.path.join(self.work_dir, filename))
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        content = ""
        try:
            logger.info(f"Crawling URL: {url}")
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            }
            response = requests.get(url, stream=True, headers=headers, timeout=30, verify=False)
            response.raise_for_status()

            content_type = response.headers.get("content-type", "")
            if "text/html" in content_type:
                # Get the content of the response
                html = "".join(chunk for chunk in response.iter_content(chunk_size=8192, decode_unicode=True))
                content = self.parse_html_to_markdown(html, url)

                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(content)
            else:
                with open(save_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                        content += chunk.decode("utf-8", errors="ignore")
            logger.debug(f"Successfully crawled: {url}, saved to: {save_path}")
        except Exception as e:
            logger.debug(f"Failed to crawl: {url}: {e}")

        return content, save_path

    def url_crawl(self, url: str) -> str:
        """
        Crawl a website and return the content of the website as a json string.

        :param url: The URL of the website to read.
        :return: str
        """
        content, save_path = self.crawl_url_to_file(url)
        crawler_result = {
            "url": url,
            "content": content,
            "save_path": save_path,
        }
        result = json.dumps(crawler_result, indent=2, ensure_ascii=False)
        return result


if __name__ == '__main__':
    m = UrlCrawlerTool()
    url = "https://www.jpmorgan.com/insights/business/business-planning/409a-valuations-a-guide-for-startups"
    r = m.url_crawl(url)
    print(url, '\n\n', r)
