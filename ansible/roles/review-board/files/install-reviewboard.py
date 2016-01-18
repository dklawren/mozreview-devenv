# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import getopt
import os
import subprocess
import sys

# parse ports from command line
bugzilla_port = 0
try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['bugzilla_port='])
    for o, a in opts:
        if o == '--bugzilla_port':
            bugzilla_port = a
    if bugzilla_port == 0:
        raise getopt.GetoptError('missing')
except getopt.GetoptError:
    print("all command line options must be provided\n\n"
          "eg. install-reviewboard.py\n"
          "  --bugzilla_port=8081\n")
    sys.exit(2)

ROOT = '/reviewboard'
os.environ['HOME'] = '%s/data' % ROOT
sys.path.insert(0, '%s/conf' % ROOT)

# Ensure settings allow proper access.
lines = open('%s/conf/settings_local.py' % ROOT, 'rb').readlines()
with open('%s/conf/settings_local.py' % ROOT, 'wb') as fh:
    # We would ideally set logging_directory via site config, but Djblets
    # isn't allowing us to set a string value to a None type. Derp.
    log_directory_found = False
    log_production_found = False
    for line in lines:
        if line.startswith(b'ALLOWED_HOSTS'):
            line = b'ALLOWED_HOSTS = ["*"]\n'
        elif line.startswith(b'PRODUCTION'):
            line = b'PRODUCTION = False\n'
            log_production_found = True
        elif line.startswith(b'DEBUG ='):
            line = b'DEBUG = True\n'
        elif line.startswith(b'LOGGING_DIRECTORY'):
            line = b'LOGGING_DIRECTORY = "/var/log/httpd"\n'
            log_directory_found = True
        fh.write(line)
    if not log_directory_found:
        fh.write('LOGGING_DIRECTORY = "/var/log/httpd"\n')
    if not log_production_found:
        fh.write('PRODUCTION = False\n')


class FakeOptions(object):
    copy_media = False

from reviewboard.cmdline.rbsite import Site
site = Site(ROOT, FakeOptions())
site.run_manage_command('syncdb', ['--noinput'])
site.setup_settings()
from reviewboard import initialize
initialize()

# toggle disable/enable to get first run code to run
print('disabling extensions')
site.run_manage_command(
    'disable-extension', ['mozreview.extension.MozReviewExtension'])
site.run_manage_command(
    'disable-extension', ['rbbz.extension.BugzillaExtension'])
site.run_manage_command(
    'disable-extension', ['rbmotd.extension.MotdExtension'])

print('enabling extensions')
site.run_manage_command(
    'enable-extension', ['mozreview.extension.MozReviewExtension'])
site.run_manage_command(
    'enable-extension', ['rbbz.extension.BugzillaExtension'])
site.run_manage_command(
    'enable-extension', ['rbmotd.extension.MotdExtension'])

print('configuring review board')
from djblets.siteconfig.models import SiteConfiguration
sc = SiteConfiguration.objects.get_current()
sc.set('auth_backend', 'bugzilla')
sc.set('auth_bz_xmlrpc_url', 'http://localhost:%s/xmlrpc.cgi' % bugzilla_port)
sc.save()

# ensure admin user is hooked up to bugzilla
from django.contrib.auth.models import User
from mozreview.models import BugzillaUserMap
u = User.objects.get(email='admin@example.com')
u.password = '!'
u.save()
try:
    BugzillaUserMap.objects.get(bugzilla_user_id=1)
except BugzillaUserMap.DoesNotExist:
    bum = BugzillaUserMap(user=u, bugzilla_user_id=1)
    bum.save()

# configure mozreview
from djblets.extensions.models import RegisteredExtension
mre = RegisteredExtension.objects.get(
    class_name='mozreview.extension.MozReviewExtension')
# XXX autoland url.  add --autoland <url>
mre.settings['autoland_import_pullrequest_ui_enabled'] = False
mre.settings['autoland_try_ui_enabled'] = False
mre.settings['autoland_testing'] = True
mre.settings['autoland_url'] = 'http://localhost:8083'
mre.settings['autoland_user'] = 'autoland'
mre.settings['autoland_password'] = 'autoland'
# ldap runs on this host
mre.settings['ldap_url'] = 'ldap://127.0.0.1:389'
mre.settings['ldap_user'] = 'uid=bind-mozreview,ou=logins,dc=mozilla'
mre.settings['ldap_password'] = 'password'
# XXX pulse - used for bots.  add --pulse host:port opt and split
mre.settings['enabled'] = False  # pulse-enabled
mre.settings['pulse_host'] = None
mre.settings['pulse_port'] = None
mre.settings['pulse_ssl'] = False
mre.settings['pulse_user'] = 'guest'
mre.settings['pulse_password'] = 'guest'
mre.save()

subprocess.check_call(['/bin/chown', '-R', 'reviewboard:reviewboard', ROOT])
