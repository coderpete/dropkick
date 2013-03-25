import os
import webbrowser

from docutils.core import publish_parts


__template__ = '''<!DOCTYPE html>
<html>
<title>%(title)s</title>

<xmp theme="%(theme)s" style="display:none;">
%(content)s
</xmp>

%(rawcontent)s

<script src="http://strapdownjs.com/v/0.2/strapdown.js"></script>
</html>
'''

__raw_content_template__ = '<div class="container" id="content">%s</div>'


def publish(connection, document, bucket, theme, prefix=None, title=None):
    bucket = connection.get_bucket(bucket)

    key_name = document.name

    if '.' in key_name:
        key_name = key_name.rsplit('.', 1)[0] + '.html'
    if '/' in key_name:
        key_name = key_name.rsplit('/', 1)[1]

    if prefix:
        key_name = '%s/%s' % (prefix, key_name)

    content = document.read()
    rawcontent = ''
    if document.name.endswith('.rst'):
        html = publish_parts(content, writer_name='html')['body']
        rawcontent = __raw_content_template__ % html
        content = ''

    content = __template__ % {
        'title': title if title else key_name,
        'content': content,
        'rawcontent': rawcontent,
        'theme': theme
    }

    key = bucket.new_key(key_name)
    key.content_type = 'text/html'
    key.set_contents_from_string(content)
    key.set_canned_acl('public-read')

    public_url = key.generate_url(0, query_auth=False, force_http=True)

    os.system('echo "%s" | pbcopy' % public_url)
    webbrowser.open_new(public_url)
