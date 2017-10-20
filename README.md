# Coverwall

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)

This tool generates an HTML page with your Spotify library album covers.
It looks like a wall of covers, hence the name 🙂 Best Tool, Great Tool!

## Dependencies

- [Spotipy](https://github.com/plamere/spotipy) to query the [Spotify API](https://developer.spotify.com/web-api/)
- [Grequests](https://github.com/kennethreitz/grequests) to download album covers
- [Click](http://click.pocoo.org) for the command line interface
- [Jinja2](http://jinja.pocoo.org) for templating

```shellsession
$ pip install -r requirements.txt
```

Or, if you're familiar with [`pipenv`](https://github.com/kennethreitz/pipenv/):

```shellsession
$ pipenv install --three
```

## Usage

You need to register an app on the [Spotify Developer website](https://developer.spotify.com/my-applications/#!/applications), then set environment variables with your credentials:

```shellsession
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
```

You can also paste this in an `.env` file and `source` it before running the script.

```shellsession
$ python coverwall.py --help
Usage: coverwall.py [OPTIONS] USER

Options:
  --template TEXT  Jinja2 template file
  --images TEXT    Download images locally in specified folder
  --no-download    Disable image downloading
  --log            Show logging information
  --playlist TEXT  Playlist ID instead of user's library
  --help           Show this message and exit.
```

### Example

```shellsession
$ python coverwall.py nothyp --template template-ghost.html
```

## Note on using the Ghost template

In order to use the Ghost template, you first need to create a static post with no content, only a title.
Then, you need to copy the generated `index.html` as `page-PostName.hbs` in `<GHOST_FOLDER>/content/themes/<YOUR_THEME>/`, where `PostName` is the title of your static post. For instance:

```shellsession
$ cp output/index.html /var/www/ghost/content/themes/casper/page-music.hbs
```
Thanks to [Christos Matskas](https://cmatskas.com/create-a-static-page-with-custom-layout-in-ghost/) for this tip.

Obviously, you also need to copy the `styles.css` file to the corresponding, for instance `/var/www/ghost/content/themes/casper/assets/built/music.css`.

## License

This project is licensed under the MIT License, see the LICENSE file for details.
