# mozreview-devenv
vagrant based development environment for mozreview.
this is my work-in-progress repo.

reasons for doing this instead of from the existing docker based environment:
- focused on a simple deployment strategy with a minimal number of moving parts
- persistent data across upgrades/provisioning
- allows pre-configuring for development (minification, logging, tools)
- grants flexibility with regards to stubbing out services, and
  reduced-but-functional deployment scenarios

non-goals:
- this is not a replacement for the docker based testing environment
  - the testing/ docker images are designed to match production's deployment
  	and deliver the best environment for running tests
- developer environment for non-mozreview/reviewboard parts of vct

installation:

- install the vagrant-triggers plugin:
  - vagrant plugin install vagrant-triggers
- copy the contents of this repo into a 'dev' directory under your vct checkout
  (ie. this file should be version-control-tools/dev/README.md).
- apply the hg_helper.patch patch
- optional: edit config.yml to set ports
- run 'vagrant up'
- add the following to .hgignore:
  - dev/env/
  - dev/test-repo/
  - dev/venv/

how it works:

reviewboard is run using django's runserver inside a screen session owned
by the 'reviewboard' user.  edit the mozreview files on your local filesystem
and refresh the page to see changes.

a test repository has been created under dev/test-repo.  create/update files
there and use "hg push" to push changes to reviewboard for review.  by default
changes are pushed as 'default@example.com', to use another user edit
dev/test-repo/.hg/hgrc and change the email address on the 'ssh=' line.

five users have been created for you: default@example.com, and
level0@example.com through level3@example.com.  use the 'create-user' script
in this directory to create new users.

if you need to restart the development reviewboard server:
- $ vagrant ssh
- [vagrant@mozreview-dev ~]$ sudo su - reviewboard
- [reviewboard@mozreview-dev ~]$ screen -r django
- (Ctrl+C)
- [screen is terminating]
- [reviewboard@mozreview-dev ~]$ ./start-reviewboard

directory structure within the vm:
- /src : nfs mount of your vct directory
- /reviewboard : reviewboard data directory
- /bugzilla : bmo
- /repo : mercurial repository

starting from scratch:
- vagrant destroy
- rm dev/env dev/test-repo dev/venv
- vagrant up
