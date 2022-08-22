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

    def __init__(self, url, config_path=f'{os.path.dirname(os.path.realpath(__file__))}/config.json'):
        self.config_path = config_path
        self.config = self.load_config()
        self.output_directory = self.config.get('outputDirectory')
        self.url = url
        self.soup = self.get_soup()
        self.gif_url = self.get_gif_url()
        self.clean_gif_url = self.clean_meta_gif_url()

    def load_config(self):
        with open(self.config_path) as config_file:
            return json.load(config_file).get('config')

    def save_gif(self, filename=time.strftime("%Y-%m-%d_%H-%M-%S"), path='/Users/matt/Desktop/gifs/'):
        try:
            r = requests.get(self.clean_gif_url)
            with open(f'{path}{filename}.gif', 'wb') as f:
                f.write(r.content)
            return filename, path
        except Exception as e:
            print(e)
            return None, None

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


def get_response(text):
    return input(text)


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

    # TODO remove comments
    # args = parser.parse_args()
    # args = parser.parse_args(
    #     ['https://giphy.com/gifs/long-far-FbPsiH5HTH1Di', '-o', '.', '-n', 'test.gif'])
    args = parser.parse_args()

    # guards against bad directory
    if args.output and not os.path.exists(args.output):
        raise Exception(f'Output directory does not exist: {args.output}\nExiting...')
        print('exception')

    # guards against overwriting existing file
    if os.path.exists(f'{args.output}/{args.name}'):
        prompt = f'File already exists: {args.output}/{args.name}\nOverwrite? *THIS CANNOT BE UNDONE* [y/N]: '
        response = get_response(prompt)

        # if enter, overwrite
        if response.lower() == 'y':
            response = 'y'
            print(give_answer(response))

        # if no, exit
        elif response == '' or response.lower() == 'n':
            print('Exiting...')
            give_answer(response)
            sys.exit()

        # if anything else, exit
        else:
            print('Exiting...')
            sys.exit()

    # raise error if args.url is not a giphy url
    if not re.search(r'(?<=giphy.com/gifs/).*', args.url):
        raise Exception('Not a valid giphy url')

    grabber = GiphyGrabber(url=args.url)
    result = grabber.save_gif(filename=args.name)
    if result:
        print(f'Saved {result[0]} to {result[1]}')
    print('Exiting...')

# TODO:
# - remove comments
# - prevent main.py error 'URL is required' when calling without args
