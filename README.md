# kaydet.link

Self-hosted bookmark sharing platform. Save links, add notes, tag them, and discover what others are saving.

## Features

- **Save links** with auto-scraped metadata (title, description, image from og: tags)
- **Personal notes and tags** on each bookmark
- **Save from others** — see a link someone saved, save it yourself with your own notes
- **Comments** on links
- **Tag-based browsing**
- **Wiki** for community documentation
- **Notifications** when someone saves your link or comments
- **Multi-language** support (English, Turkish)
- **Self-hosted** — run your own instance with your own domain

## Quick Start

```bash
# clone
git clone https://github.com/miratcan/kaydet.link.git
cd kaydet.link

# install dependencies (requires Python 3.13+ and uv)
uv sync

# run migrations
uv run python manage.py migrate

# create a superuser
uv run python manage.py createsuperuser

# (optional) load sample data
uv run python manage.py seed_data

# run the dev server
uv run python manage.py runserver
```

Open http://localhost:8000 in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

```bash
cp .env.example .env
```

All settings can be configured via environment variables or the `.env` file. See `.env.example` for available options.

### Key settings

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | insecure dev key | **Set in production** |
| `DJANGO_DEBUG` | `True` | Set to `False` in production |
| `DJANGO_ALLOWED_HOSTS` | `*` | Comma-separated hostnames |
| `SITE_NAME` | `kaydet.link` | Displayed in header and emails |
| `DATABASE_URL` | `sqlite:///db.sqlite3` | Database connection string |
| `LANGUAGE_CODE` | `en` | Default language (`en` or `tr`) |
| `TIME_ZONE` | `UTC` | Server timezone |

## Production Deployment

```bash
# install with production dependencies
uv sync --extra prod

# set environment variables
export DJANGO_SECRET_KEY=your-secret-key
export DJANGO_DEBUG=False
export DJANGO_ALLOWED_HOSTS=yourdomain.com
export DATABASE_URL=postgres://user:pass@localhost:5432/kaydetlink

# collect static files
uv run python manage.py collectstatic --noinput

# run migrations
uv run python manage.py migrate

# run with gunicorn
uv run gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## Tech Stack

- **Python 3.13+** / **Django 6**
- **SQLite** (default) or **PostgreSQL**
- **htmx** for interactive UI without JavaScript frameworks
- **WhiteNoise** for static file serving
- **markdown-it-py** + **nh3** for safe Markdown rendering
- **django-environ** for configuration

## Development

```bash
# install dev dependencies
uv sync --extra dev

# run tests
uv run python manage.py test

# run linter
uv run ruff check .

# generate translations
cd core && uv run python ../manage.py makemessages -l tr && cd ..
uv run python manage.py compilemessages --locale=tr
```

## License

MIT — see [LICENSE](LICENSE).

## Credits

Inspired by [LinkFloyd](https://github.com/linkfloyd/linkfloyd-museum), a link sharing community from 2012. The legacy codebase is included as a git submodule for reference.

See [credits.md](credits.md) for additional attributions.
