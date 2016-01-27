config = "/repo/hg/mozilla/test-repo"

# Uncomment to send python tracebacks to the browser if an error occurs:
# import cgitb; cgitb.enable()

# enable demandloading to reduce startup time
from mercurial import demandimport
demandimport.enable()

from mercurial.hgweb import hgweb
application = hgweb(config)
