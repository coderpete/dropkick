import logging
import dropkick.share

from cliff.command import Command


class ShareFiles(Command):
    """Publishes an encrypted ZIP file."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ShareFiles, self).get_parser(prog_name)
        parser.add_argument('share',
                help='The path to your directory to share.')
        parser.add_argument('--name', required=True,
                help='The name to give the zipped object.')
        parser.add_argument('--bucket', required=True,
                help='The bucket to publish to.')
        parser.add_argument('--password', required=False,
                help='An optional password.')
        return parser

    def take_action(self, parsed_args):
        dropkick.share.share(
            self.app.connection,
            parsed_args.share,
            parsed_args.bucket,
            parsed_args.name,
            parsed_args.password
        )
