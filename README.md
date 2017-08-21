# Coverwall

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)

This tool generates an HTML page with your Spotify library album covers.
It looks like a wall of covers, hence the name 🙂

## Dependencies

```shellsession
$ pip install -r requirements.txt
```

Or, if you're familiar with [`Pipenv`](https://github.com/kennethreitz/pipenv/):

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
  --help           Show this message and exit.
```

### Example

```shellsession
$ python coverwall.py nothyp --template template-ghost.html
```

## License

This project is licensed under the MIT License, see the LICENSE file for details.
