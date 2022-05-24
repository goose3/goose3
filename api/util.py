import redis, json
import zlib
from bs4 import BeautifulSoup
from goose3 import Goose


class RawHtmlFetcher:
    def __init__(self, redis_url, data_key):
        self.redis_url = redis_url
        self.data_key = data_key

    def acquire(self):
        redis_client = redis.from_url(self.redis_url)
        compressed_data = redis_client.get(self.data_key)
        try:
            result = zlib.decompress(compressed_data)
        except zlib.error:
            result = compressed_data

        if result:
            return json.loads(result)
        else:
            return None


class GooseAPI:
    def __init__(self, url, raw_html=None):
        self.url = url
        self.raw_html = raw_html
        self.goose = Goose()
        self.extracted_content = None

    def extract(self):
        self.extracted_content = self.goose.extract(
            url=self.url, raw_html=self.raw_html
        )
        extracted_data = {
            "title": self.extracted_content.title,
            "summary": self.extracted_content.meta_description,
            "plain_text": self.extracted_content.cleaned_text,
            "published_at": self.extracted_content.publish_date,
            "assets": self.videos() + self.audios(),
        }
        return extracted_data

    # yet to rewrite
    def images(self):
        images = []
        for image in self.extracted_content._top_image:
            images.append(
                {
                    "url": image.src,
                    "width": image.width,
                    "height": image.height,
                    "type": "image",
                }
            )
            print("images are", images)
        return images

    def videos(self):
        videos = []
        for video in self.extracted_content.movies:
            videos.append(
                {
                    "url": video.src,
                    "width": video.width,
                    "height": video.height,
                    "type": "video",
                }
            )

        return videos

    def tags(self):
        tags = self.extracted_content.meta_keywords.split(",")
        return filter(None, [tag.strip() for tag in tags])

    def audios(self):
        audios = set()
        soup = BeautifulSoup(self.extracted_content.raw_html, "html.parser")
        audio_links = soup.find_all("audio")
        source_links = soup.find_all("source")
        embed_links = soup.find_all("embed")
        object_links = soup.find_all("object")

        for link in audio_links:
            if link.has_attr("src"):
                audio = link["src"].replace("\t", "")
                if audio.startswith("http"):
                    audios.add(audio)
                else:
                    new_link = self.get_domain() + link["src"].replace("\t", "")
                    audios.add(new_link)

        for link in source_links:
            if link.has_attr("src"):
                if link.has_attr("type"):
                    if link["type"].startswith("audio"):
                        audio = link["src"].replace("\t", "")
                        if audio.startswith("http"):
                            audios.add(audio)
                        else:
                            new_link = self.get_domain() + link["src"].replace("\t", "")
                            audios.add(new_link)
                else:
                    audio = link["src"].replace("\t", "")
                    if audio.startswith("http"):
                        audios.add(audio)
                    else:
                        new_link = self.get_domain() + link["src"].replace("\t", "")
                        audios.add(new_link)

        for link in embed_links:
            if link.has_attr("src"):
                audio = link["src"].replace("\t", "")
                if audio.startswith("http"):
                    audios.add(audio)
                else:
                    new_link = self.get_domain() + link["src"].replace("\t", "")
                    audios.add(audio)

        for link in object_links:
            if link.has_attr("data"):
                audio = link["data"].replace("\t", "")
                if audio.startswith("http"):
                    audios.add(audio)
                else:
                    new_link = self.get_domain() + link["data"].replace("\t", "")
                    audios.add(new_link)

        final_audio_list = []
        for i in audios:
            final_audio_list.append({"url": i, "type": "audio"})

        return final_audio_list

    def get_domain(self):
        req_url = ""
        count = 0
        for ch in self.url:
            if ch == "/":
                count += 1
            if count == 3:
                break
            req_url = req_url + ch
        return req_url
