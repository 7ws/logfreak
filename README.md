Log Freak
=========

This project is meant to log everything in one's life. The key goal is to let
the user go back in time -- and into present too -- and have a better
understanding of how things are turning out.


## Current support:

_Oh come back again in a few days! It's all an intense work in progress right
now._


## Planned support:

- SMS
- Call logs (including audio)
- E-mails
- Events from Google Calendar
- Posts from Twitter
- Activity on Facebook
- Activity on Google Plus
- Pictures taken at Google Photos
- Pictures taken at Instagram
- Conversations from Hangouts
- Conversations from Whatsapp
- Conversations from Telegram
- Conversations from Skype
- _(please share your idea)_


## Contributing

This is an open source project and you might prefer to run it on your own. So
here are the basic how-to.


### Installation

First, you might want to customize a few settings by setting environment
variables. Or just writing them to a `.env` file. The available options are:

- `ALLOWED_HOSTS`: A comma-separated list of domains (FQDNs) that the
  application will be accessed from. Defaults to `'*'`.
- `DATABASE_URL`: The URL to your database in a [special format][2]. Defaults
  to `'sqlite:///db.sqlite3'`.
- `DEBUG`: Debug mode. Defaults to `'True'`.
- `LANGUAGE_CODE`: The language code to get the application translated to.
  Defaults to `'en-us'`. Mind the language availability.
- `SECRET_KEY`: A long, powerful and unique random mix of weird chars. It will
  be used to salt password hashes and other security-wise stuff. Please don't
  share it anywhere!
- `STATIC_URL`: The URL on which static files will be available, with a
  trailing slash. Defaults to `'/static/'`.
- `TIME_ZONE`: The most adequate time zone for your application instance. Check
  [available options][3]. Defaults to `'America/Sao_Paulo'`.

Note that none of these are required in order to run the application in a local
development environment, though I **highly** recommend you to set them for
production.

Then, assuming you have cloned this repository and got an active
[virtualenv][1] running Python 3.5, you must begin with our magical `make`
script:

	(my_env)$ make setup

> **Note** that you should run the command above whenever you update your local
> repository from the mainstream. This will keep any local dependencies up to
> date and run occasional required migration tasks.


### Running

From now on you should be able to run a development server locally using the
well known Django's `runserver`:

	(my_env)$ ./manage.py runserver

And that's it. Of course, for a production environment, you'll want to use a
different stack of software and/or infrastructure to serve your application.
Check out the [Django documentation][4] for details and be careful.


### Testing

All the current tests are written in a very simple manner thanks to
[pytest][5]. To check all the unit tests, just run it:

	(my_env)$ py.test -vs

> **Note** that the arguments `-vs` are meant to make the tests output more
> verbose and let any text come into the stdout normally.

### Misc

Oh and I need coffee to continue writing this. And money to buy me coffee.
That's all folks.


## Licensing

This software is available under the GNU GPLv3 license. Please see the
[LICENSE](./LICENSE) file and/or read the [full license][6].


[1]: http://docs.python-guide.org/en/latest/dev/virtualenvs/
[2]: https://github.com/kennethreitz/dj-database-url#url-schema
[3]: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
[4]: https://docs.djangoproject.com/es/1.9/howto/deployment/
[5]: http://pytest.org/latest/
[6]: http://www.gnu.org/licenses/gpl.txt
