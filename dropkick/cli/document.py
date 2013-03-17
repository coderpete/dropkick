import logging
import dropkick.document

from cliff.command import Command


class PublishDocument(Command):
    """Publishes a Markdown document"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(PublishDocument, self).get_parser(prog_name)
        parser.add_argument('document',
                help='The path to your markdown document.')
        parser.add_argument('--theme', required=False,
                choices=['Amelia', 'Cerulean', 'Cyborg', 'Journal', 'Readable',
                    'Simplex', 'Slate', 'Spacelab', 'Spruce', 'Superhero',
                    'United'],
                default='Simplex',
                help='The theme to use to render your document.')
        parser.add_argument('--title', required=False,
                help='The title to give the document.')
        parser.add_argument('--prefix', required=False,
                help='A prefix to give to the object key. Useful for publishing into "folders."')
        parser.add_argument('--bucket', required=True,
                help='The bucket to publish to.')
        return parser

    def take_action(self, parsed_args):
        dropkick.document.publish(
            self.app.connection,
            open(parsed_args.document, 'rb'),
            parsed_args.bucket,
            parsed_args.theme,
            parsed_args.prefix,
            parsed_args.title
        )
