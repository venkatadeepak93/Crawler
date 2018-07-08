from rest_framework.views import APIView
from rest_framework.response import Response
from bs4 import BeautifulSoup
import urllib.request as urllib
import re
import json

class ImageView(APIView):
    def get(self, request):
        seed_url = request.GET.get('seed_url')
        depth = request.GET.get('depth')
        image_collector = ImageCollecter(seed_url, depth)
        image_links = image_collector.fetch_image_links()
        if image_links['urls_and_images'] == []:
            image_links['message'] = 'No images found in the seed url through the specified depth.'
        else:
            image_links['message'] = 'Success!. Please see below for images found in the seed url through the specified depth.'
        image_links = json.dumps(image_links)
        return Response(image_links)

class ImageCollecter(object):
    def __init__(self, seed_url, depth=0):
        self.seed_url = seed_url
        self.depth = depth

    def fetch_image_links(self):
        image_links = {}
        urls_and_images = []
        visited = []
        all_urls = [self.seed_url]
        depth = 0

        while(depth <= int(self.depth) and all_urls != [] ):
            sub_urls = []
            for url in all_urls:
                if url not in visited:
                    url_image_pair = {}
                    url_image_pair['url'] = url
                    url_image_pair['depth'] = depth
                    images_in_url = self.fetch_images(url)
                    links_in_url = self.fetch_links(url)
                    sub_urls.extend(links_in_url)
                    url_image_pair['images'] = images_in_url
                    if images_in_url != []:
                        urls_and_images.append(url_image_pair)
                    visited.append(url)
            if (set(sub_urls) < set(visited)) or (set(sub_urls) == set(visited)):
                all_urls = []
            else:
                all_urls = sub_urls
            depth += 1

        image_links['urls_and_images'] = urls_and_images
        return image_links

    def fetch_images(self,url):
        images_in_url = []
        try:
            html_page = urllib.urlopen(url)
            soup = BeautifulSoup(html_page, "html.parser")
            for image in soup.findAll('img', attrs={'src': re.compile("^http")}):
                images_in_url.append(image.get('src'))
        except:
            pass

        return images_in_url

    def fetch_links(self, url):
        links_in_url = []
        try:
            html_page = urllib.urlopen(url)
            soup = BeautifulSoup(html_page, "html.parser")
            links = soup.findAll('a')
            for link in links:
                if link.attrs['href'].startswith('/'):
                    links_in_url.append(self.seed_url+link.get('href'))
                elif link.attrs['href'].startswith('http'):
                    links_in_url.append(link.get('href'))
        except:
            pass

        return links_in_url