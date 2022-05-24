import requests
import bs4
import os
import sys
import time
import re
import json
import argparse


class GiphyGrabber():
    # save content of "config.json" to a variable

    def __init__(self, config_path, url):
        self.config_path = config_path or 'config.json'
        self.config = self.load_config()
        self.output_directory = self.config.get('outputDirectory')
        self.url = url
        self.soup = self.get_soup()
        self.gif_url = self.get_gif_url()
        self.clean_gif_url = self.clean_meta_gif_url()

    def load_config(self):
        with open(self.config_path) as config_file:
            return json.load(config_file).get('config')

    def save_gif(self, title=time.strftime("%Y-%m-%d_%H-%M-%S")):
        r = requests.get(self.clean_gif_url)
        with open(f'/Users/matt/Desktop/gifs/{title}.gif', 'wb') as f:
            f.write(r.content)

    def get_soup(self):
        r = requests.get(self.url)
        return bs4.BeautifulSoup(r.text, 'html.parser')

    def get_gif_url(self):
        gif_url = self.soup.find('meta', {'property': 'og:image'})['content']
        return gif_url

    def clean_meta_gif_url(self):
        return re.sub(r'(.+?)\?cid.+', r'\1', self.gif_url)

    def get_gif_image_url(self):
        return self.get_gif_image_url_from_url(self.get_gif_url())

    def get_gif_image_url_from_url(self, url):
        r = requests.get(url)
        x = re.search(r'(?<=src=").*?(?=")', r.text)
        return x.group(0)


def get_response(prompt):
    return input(prompt)


def give_answer(answer):
    switch = {
        'y': 'Overwriting...',
        'n': 'Exiting...',
    }
    return switch.get(answer)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='giphygrab - save a GIF today!')
    parser.add_argument('url', help='url to GIF (e.g. https://giphy.com/gifs/long-far-FbPsiH5HTH1Di)')
    parser.add_argument('-n', '--name', help='filename to save GIF as (default: giphygrab<time>.gif)',
                        default=f'giphygrab{time.strftime("%Y%m%d_%H%M%S")}')
    parser.add_argument('-o', '--output',
                        help='Path of the output directory (default is defined in config.json)')

    # args = parser.parse_args()
    args = parser.parse_args(
        ['https://giphy.com/gifs/long-far-FbPsiH5HTH1Di', '-o', '.', '-n', 'test.gif'])
    print(args)

    # guards against bad directory
    if args.output and not os.path.exists(args.output):
        raise Exception(f'Output directory does not exist: {args.output}\nExiting...')
        print('exception')

    # guards against overwriting existing file
    if os.path.exists(f'{args.output}/{args.name}'):
        response = get_response(f'File already exists: {args.output}/{args.name}\nOverwrite? [y/N]: ')
        # if enter, overwrite
        if response == '' or response.lower() == 'y':
            response = 'y'
            print(give_answer(response))
        # if no, exit
        elif response.lower() == 'n':
            print('Exiting...')
            give_answer(response)
            sys.exit()
        # if anything else, exit
        else:
            print('Exiting...')
            sys.exit()

    # raise error if args.url is not a giphy url
    # if not re.search(r'(?<=giphy.com/gifs/).*', args.url):
    #     raise Exception('Not a valid giphy url')

    # grabber = GiphyGrabber(url=args.url)
    # grabber.save_gif(title)
    # print('GIF saved in /Users/matt/Desktop/gifs/')
