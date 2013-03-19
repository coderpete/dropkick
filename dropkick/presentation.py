import mimetypes
import os
import pkgutil
import sys
import threading
import time
import webbrowser


# define required resources
__reveal_resources__ = [
    'reveal/css/print/paper.css', 'reveal/css/print/pdf.css',
    'reveal/css/reveal.css', 'reveal/css/reveal.min.css',
    'reveal/css/theme/beige.css', 'reveal/css/theme/default.css',
    'reveal/css/theme/moon.css', 'reveal/css/theme/night.css',
    'reveal/css/theme/serif.css', 'reveal/css/theme/simple.css',
    'reveal/css/theme/sky.css', 'reveal/css/theme/solarized.css',
    'reveal/js/reveal.js', 'reveal/js/reveal.min.js',
    'reveal/lib/css/zenburn.css', 'reveal/lib/font/league_gothic-webfont.eot',
    'reveal/lib/font/league_gothic-webfont.svg',
    'reveal/lib/font/league_gothic-webfont.ttf',
    'reveal/lib/font/league_gothic-webfont.woff',
    'reveal/lib/font/league_gothic_license', 'reveal/lib/js/classList.js',
    'reveal/lib/js/head.min.js', 'reveal/lib/js/html5shiv.js',
    'reveal/plugin/highlight/highlight.js',
    'reveal/plugin/markdown/markdown.js', 'reveal/plugin/markdown/showdown.js',
    'reveal/plugin/multiplex/client.js', 'reveal/plugin/multiplex/index.js',
    'reveal/plugin/multiplex/master.js', 'reveal/plugin/notes/notes.html',
    'reveal/plugin/notes/notes.js', 'reveal/plugin/notes-server/client.js',
    'reveal/plugin/notes-server/index.js',
    'reveal/plugin/notes-server/notes.html',
    'reveal/plugin/postmessage/postmessage.js',
    'reveal/plugin/print-pdf/print-pdf.js', 'reveal/plugin/remotes/remotes.js',
    'reveal/plugin/search/search.js', 'reveal/plugin/zoom-js/zoom.js'
]


# define templates
__template__ = pkgutil.get_data('dropkick', 'templates/presentation.html')

__section_template__ = '''<section data-markdown>
<script type="text/template">
%(content)s
</script>
</section>
'''

__container_template__ = '''<section>
%(content)s
</section>
'''


class ProgressBar(threading.Thread):
    def finish(self):
        self.finished = True

    def run(self):
        while not getattr(self, 'finished', False):
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1)


def generate(markdown_file):
    markdown = markdown_file.read()

    # parse headers
    headerlines, markdown = markdown.split('==', 1)
    headerlines = headerlines.split('\n')
    headers = dict([[value.strip() for value in line.split(':')]
                    for line in headerlines if line])

    # split into sections
    sections = markdown.split('\n\n==\n\n')
    content = []

    # iterate through sections and generate content
    for section in sections:
        parts = section.split('\n\n--\n\n')

        sectioncontent = []
        for part in parts:
            sectioncontent.append(__section_template__ % {
                'content': part
            })

        if len(parts) == 1:
            content.append(''.join(sectioncontent))
        else:
            content.append(__container_template__ % {
                'content': ''.join(sectioncontent)
            })

    # join content and render template
    headers['content'] = ''.join(content)
    return __template__ % headers


def upload_content(connection, bucket, key, content):
    # determine content type
    content_type = mimetypes.guess_type(key)[0]

    # create the object and set its content
    bucket = connection.get_bucket(bucket)
    key = bucket.new_key(key)
    if content_type:
        key.content_type = content_type
    key.set_contents_from_string(content)

    # make publicly visible
    key.set_canned_acl('public-read')

    return key


def publish(connection, presentation, bucket, name):
    # create a progress bar
    progress_bar = ProgressBar()
    progress_bar.start()

    # generate and upload the index file
    object_name = '%s/index.html' % name
    content = generate(open(presentation + os.sep + 'index.md', 'rb'))
    index_key = upload_content(connection, bucket, object_name, content)

    # upload any bundled content
    for container, _, children in os.walk(presentation):
        for child in children:
            path = '%s/%s' % (container, child)
            key_name = path.replace(presentation, name, 1)
            content = open(path, 'rb').read()
            upload_content(connection, bucket, key_name, content)

    # upload the dependent reveal files
    for resource in __reveal_resources__:
        content = pkgutil.get_data('dropkick', 'resources/%s' % resource)
        key_name = '%s/%s' % (name, resource)
        upload_content(connection, bucket, key_name, content)

    # signal completion
    progress_bar.finish()

    # open in the browser
    public_url = index_key.generate_url(0, query_auth=False, force_http=True)
    os.system('echo "%s" | pbcopy' % public_url)
    webbrowser.open_new(public_url)

    # print out a message
    print
    print 'Your presentation is now available at:', public_url
