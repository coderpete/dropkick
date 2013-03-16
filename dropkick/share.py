import os

from cStringIO import StringIO


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
    os.system('zip -r %(zip-name)s.zip %(password)s %(directory)s' % {
        'zip-name': name,
        'password': ('--password="%s"' % password) if password else '',
        'directory': directory
    })
    return open('%s.zip' % name, 'rb').read()


def share(connection, path, bucket, name, password):
    # create the zip file
    zipped_data = create_zip(path, name, password)

    # upload the file
    key = upload_content(connection, bucket, '%s.zip' % name, zipped_data)

    # open in the browser
    public_url = key.generate_url(0, query_auth=False, force_http=True)
    os.system('echo "%s" | pbcopy' % public_url)

    # output to the console
    print 'Your file is now available at: %s' % public_url
