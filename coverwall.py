import io
import logging
import os
import re

import click
import grequests
import jinja2

import spotipy
import spotipy.util

NUMBER_OF_ALBUMS = 300
LIMIT = 50

OUTPUT_HTML = 'output/index.html'
TEMPLATE = 'template.html'

DOWNLOAD_IMAGES = True
IMAGES_FOLDER = 'output/img/'
IMAGES_EXT = '.png'


def clean(text):
    """
    Remove useless stuff like "Deluxe Edition" from album names.

    >>> clean("Album (Deluxe Edition)")
    'Album'
    >>> clean("Album (Test) (Deluxe)")
    'Album (Test)'
    """

    patterns = ['\(\w+ Edition\)',
                '\(\w+ Version\)',
                '\(Deluxe\)'
                ]

    for p in patterns:
        text = re.sub(p, '', text)

    text = text.rstrip()

    return text


def auth(username, scope):
    token = spotipy.util.prompt_for_user_token(username, scope)

    if not token:
        raise Exception("Couldn't get auth token.")

    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    logging.info('Logged in as %s' % (sp.me()['id']))

    return sp


def query_albums(sp, n, limit):
    albums = []
    results = {"items": []}
    limit = min(n, limit)

    for i in range(0, int(n / limit)):
        result = sp.current_user_saved_tracks(limit=limit, offset=i * limit)
        results["items"] += result["items"]

    for i, item in enumerate(results["items"]):
        artist = item['track']['artists'][0]['name']
        name = clean(item['track']['album']['name'])
        cover = item['track']['album']['images'][0]['url']

        album = {'artist': artist, 'name': name, 'cover': cover}

        if not any(album.get('name', None) == name for album in albums):
            logging.info('Album: %s' % (album['name'], ))
            albums.append(album)

    return albums


def download_images(albums, path, ext):
    urls = []

    for album in albums:
        img = album['cover'].split('/')[-1]
        img_path = path + img + ext

        if not os.path.isfile(img_path):
            logging.info('New image found: %s' % (img_path, ))
            urls.append(album['cover'])

        album['cover'] = '/'.join(img_path.split('/')[1:])

    rs = (grequests.get(u) for u in urls)
    m = grequests.map(rs)

    for r in m:
        img_path = path + r.url.split('/')[-1] + ext
        with io.open(img_path, 'wb') as f:
            logging.info('Saving image %s' % (img_path, ))
            f.write(r.content)

    return len(m)


def render(albums, output_file, tpl_file):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('./'))
    template = env.get_template(tpl_file)

    with open(output_file, 'w') as f:
        logging.info('Rendering output HTML file %s' % (output_file, ))
        f.write(template.render(albums=albums))


@click.command()
@click.option('--template', default=False, help='Jinja2 template file')
@click.option('--images', default=False, help='Download images locally in specified folder')
@click.option('--log', is_flag=True, help='Show logging information')
@click.argument('user')
def main(template, images, log, user):
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if log:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)

    if images:
        if not os.path.isdir(images):
            logging.error('Image folder does not exist: %s' % (images, ))
            raise OSError('Image folder does not exist: %s' % (images, ))

        if not images.endswith('/'):
            images += ('/')
        images_folder = images
    else:
        images_folder = IMAGES_FOLDER

    if template:
        if not os.path.isfile(template):
            logging.error('Template does not exist: %s' % (template, ))
            raise OSError('Template does not exist: %s' % (template, ))
    else:
        template = TEMPLATE

    scope = "user-library-read"

    sp = auth(user, scope)
    albums = query_albums(sp, NUMBER_OF_ALBUMS, LIMIT)

    if DOWNLOAD_IMAGES:
        logging.info('Downloading cover images')
        img_nb = download_images(albums, images_folder, IMAGES_EXT)

    render(albums, OUTPUT_HTML, template)

    logging.info('Retrieved %d albums and %d images.' % (len(albums), img_nb))


if __name__ == "__main__":
    main()
