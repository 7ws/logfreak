Log Freak
=========

This project is meant to log everything in one's life. The key goal is to let
the user go back in time -- and into present too -- and have a better
understanding of how things are turning out.


## Current support:

- SMS (partial)
- Twitter (partial)


## Planned support:

- Call logs (including audio)
- E-mails
- Events from Google Calendar
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

This projects uses [bower][7] for managing third-party static files libraries.
Please make sure you have an up-to-date version of it installed and available
in your `$PATH`:

	$ bower --version

As for connecting to third-party API services, the following configuration keys
are available:

- `TWITTER_CONSUMER_TOKEN`: The consumer token provided by Twitter.
- `TWITTER_CONSUMER_TOKEN`: The consumer secret provided by Twitter.

> **Note** that none of the above is required in order to quick-start the
> project, but obviously not every third-party related module will work. It is
> important to check [`settings/security.py`](.settings/security.py) for
> details on each service.


### Running

From now on you should be able to run a development server locally:

	(my_env)$ make dev

> **Note** that this command will run a couple commands simultaneously: 1.
> start a local Redis server with default parameters, 2. start the `rqworker`
> command to handle parallel job queues and 3. finally, bound to capturing
> keystrokes, our modified version of Django's `runserver`. You should not use
> this `make` command if you intend to develop using different configurations.

And that's it. Of course, for a production environment, you'll want to use a
different stack of software and/or infrastructure to serve your application.
Check out the [Django documentation][4] for details and be careful.


### Testing

All the current tests are written in a very simple manner thanks to
[pytest][5]. To check all the unit tests, just run it:

	(my_env)$ py.test -vs

> **Note** that the arguments `-vs` are meant to make the tests output more
> verbose and let any text come into the stdout normally.


### Design notes

There are some important design decisions made to better organize this project.
Some of them bypass default Django recommended structure, but greatly improve
the modularization of all applications on this specific project. The main point
is to take advantage of the core features from Django while having our own
structure, pure-Python like.

1. **Apps are not independent**. While following the _Don't Repeat Yourself_
   principle heavily, the "one big app" is split into several core apps
   (`backend.*`). This breaks the default Django design recommendation, but
   gives us an advantage on organization of code and assets.
2. **Front-end is separated from the core apps**. While the core apps
   (`backend.*`) will provide us base functionality, front-end code related to
   web views live in the [`/static` directory](/static). The `backend.webview`
   app will rely on it, leaving Django's `AppDirectoriesFinder` useless. Note
   that it can't be disabled in order to keep support for 3rd-party apps.


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
[7]: http://bower.io/
