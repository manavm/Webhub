import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True
SECRET_KEY = 'K\x17\xee\xf9\xdcW\x9e\xf6\x92Y\xd9\xdf\xa1\xfeB%}\xa0\xf5,N\x80\x81\xdd\x1c\x88FK\xad.'

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' },
    { 'name': 'Wordpress', 'url': 'https://username.wordpress.com/'}
    ]

MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = 'mmandhani@teslamotors.com'
MAIL_PASSWORD = 'Meatut2015'

ADMINS = ['mmandhani@teslamotors.com']