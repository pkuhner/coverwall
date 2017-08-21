# Coverwall

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)

This tool generates an HTML page with your Spotify library cover albums.
It looks like a wall of covers, hence the name 🙂

## Dependencies

```
$ pip install -r requirements.txt
```

Or, if you're familiar with [`Pipenv`](https://github.com/kennethreitz/pipenv/):

```
$ pipenv install --three
```

## Usage

```
$ python coverwall.py --help
Usage: coverwall.py [OPTIONS] USER

Options:
  --template TEXT  Jinja2 template file
  --images TEXT    Download images locally in specified folder
  --no-download    Disable image downloading
  --log            Show logging information
  --help           Show this message and exit.
```
