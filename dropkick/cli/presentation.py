import logging
import dropkick.presentation

from cliff.command import Command


class PublishPresentation(Command):
    """Publishes a Markdown presentation"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(PublishPresentation, self).get_parser(prog_name)
        parser.add_argument('presentation',
                help='The path to your markdown presentation bundle.')
        parser.add_argument('--bucket', required=True,
                help='The bucket to publish to.')
        parser.add_argument('--name', required=True,
                help='The URI compatible name to publish to.')
        return parser

    def take_action(self, parsed_args):
        dropkick.presentation.publish(
            self.app.connection,
            parsed_args.presentation,
            parsed_args.bucket,
            parsed_args.name
        )
