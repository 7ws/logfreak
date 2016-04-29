import subprocess

from django.contrib.staticfiles.management.commands.runserver import (
    Command as BuiltinRunserverCommand)


class Command(BuiltinRunserverCommand):

    """Extend the built-in runserver with common pre-routines
    """

    def bower_install(self):
        """Install 3rd-party static assets through Bower
        """
        self.stdout.write('Installing Bower components...')
        subprocess.run(
            'bower install',
            shell=True,
            stdout=self.stdout,
            stderr=self.stderr)
        self.stdout.write('\n')  # Separate output

    def inner_run(self, *args, **kwargs):
        self.bower_install()
        super(Command, self).inner_run(*args, **kwargs)
