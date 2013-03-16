import os
import urllib
import webbrowser

from cStringIO import StringIO


__email_template__ = '''I've got something to share with you. Download it here:

    %(link)s

%(password)s
'''

def upload_content(connection, bucket, key, content):
    # create the object and set its content
    bucket = connection.get_bucket(bucket)
    key = bucket.new_key(key)
    key.content_type = 'application/zip'
    key.set_contents_from_string(content)

    # make publicly visible
    key.set_canned_acl('public-read')

    return key


def create_zip(path, name, password):
    parent, directory = os.path.split(path)
    os.chdir(parent)
    os.system('zip -r %(zip-name)s.zip %(password)s %(directory)s > /dev/null' % {
        'zip-name': name,
        'password': ('--password="%s"' % password) if password else '',
        'directory': directory
    })
    return open('%s.zip' % name, 'rb').read()


def share(connection, path, bucket, name, password, email):
    # create the zip file
    zipped_data = create_zip(path, name, password)

    # upload the file
    key = upload_content(connection, bucket, '%s.zip' % name, zipped_data)

    # open in the browser
    public_url = key.generate_url(0, query_auth=False, force_http=True)
    os.system('echo "%s" | pbcopy' % public_url)

    # output to the console
    print 'Your file is now available at: %s' % public_url

    # optionally open an email
    if email:
        mailto = 'mailto:%(email)s?body=%(body)s&subject=%(subject)s' % {
            'email': email,
            'subject': 'Something to share with you',
            'body': __email_template__ % {
                'link': public_url,
                'password': (
                    'Use the password %s to open the file.' % password
                ) if password else ''
            }
        }
        webbrowser.open_new(mailto)
