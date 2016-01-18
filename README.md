# mozreview-devenv
vagrant based development environment for mozreview.
this is my work-in-progress repo.

to install copy the contents of this repo into a 'vagrant' directory under your
vct checkout (ie. this file should be version-control-tools/vagrant/README.md).

reasons for doing this instead of from the existing docker based environment:
- focused on a simple deployment strategy with a minimal number of moving parts
- persistent data across upgrades/provisioning
- allows preconfiguring for development (minification, logging, tools)
- grants flexibility with regards to stubbing out services, and
  reduced-but-functional deployment scenarios

non-goals:
- this is not a replacement for the docker based testing environment
  - the testing/ docker images are designed to match production's deployment
  	and deliver the best environment for running tests
- developer environment for non-mozreview/reviewboard parts of vct

installation:

optional: edit config.yml to set the ports
run 'vagrant up'