import json
import logging
import sys
import os
import boto

from cliff.app import App
from cliff.commandmanager import CommandManager


class DropkickApp(App):
    """Dropkick main application"""

    log = logging.getLogger(__name__)

    def __init__(self):
        super(DropkickApp, self).__init__(
            description='dropkick',
            version='0.1.0',
            command_manager=CommandManager('dropkick.cli')
        )
        self.config = {}

    @property
    def config_file_path(self):
        return os.environ['HOME'] + os.sep + '.dropkick'

    def initialize_app(self, argv):
        self.log.debug('initialize_app')
        if os.path.exists(self.config_file_path):
            self.config = json.loads(open(self.config_file_path, 'rb').read())
            self.initialize_connection()

    def initialize_connection(self):
        self.connection = boto.connect_s3(
            aws_access_key_id=self.config['access_key'],
            aws_secret_access_key=self.config['secret_key'],
            host='objects.dreamhost.com'
        )

    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)

    def set_credentials(self, access_key, secret_key):
        self.config['access_key'] = access_key
        self.config['secret_key'] = secret_key
        open(self.config_file_path, 'wb').write(json.dumps(self.config))


def main(argv=sys.argv[1:]):
    app = DropkickApp()
    return app.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
