import logging

from cliff.command import Command


class Configure(Command):
    """Configures the DreamObjects credentials."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Configure, self).get_parser(prog_name)
        parser.add_argument('--access-key', dest='access_key', required=True,
                help='Your DreamObjects S3 Access Key')
        parser.add_argument('--secret-key', dest='secret_key', required=True,
                help='Your DreamObjects S3 Secret Key')

        return parser

    def take_action(self, parsed_args):
        self.app.set_credentials(
                access_key=parsed_args.access_key,
                secret_key=parsed_args.secret_key)
