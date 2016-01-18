Vagrant.require_version ">= 1.7.0"

require 'yaml'
current_dir    = File.dirname(File.expand_path(__FILE__))
configs        = YAML.load_file("#{current_dir}/config.yml")

Vagrant.configure(2) do |config|
  # XXX this box is untested
  config.vm.box = "puppetlabs/centos-7.2-64-nocm"
  # XXX add providers for vmware and virtualbox
  #config.vm.provider :virtualbox do |vb, override|
  #config.vm.provider :vmware_workstation do |vmf, override|
  #config.vm.provider :vmware_fusion do |vmf, override|

  config.vm.provider :parallels do |prl, override|
    override.vm.box = "parallels/centos-7.2"
    prl.name = "mozreview-dev"
    prl.update_guest_tools = true
    prl.memory = 1024
    prl.cpus = 2
  end

  config.vm.hostname = "mozreview-dev"
  # in order for auth delegation to work reviewboard and bugzilla need to use
  # the same port for internal and external requests
  config.vm.network :forwarded_port, guest: configs['REVIEWBOARD_PORT'], host: configs['REVIEWBOARD_PORT']
  config.vm.network :forwarded_port, guest: configs['BUGZILLA_PORT'], host: configs['BUGZILLA_PORT']

  if configs['FORWARD_LDAP']
    # mapping ldap is optional, and may be useful for debugging
    config.vm.network :forwarded_port, guest: 389, host: 389
  end

  config.vm.synced_folder "../", "/src", :nfs => true

  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "ansible/dev-environment.yml"
    ansible.extra_vars = 'config.yml'
    ansible.verbose = configs['VERBOSE']
  end

  # XXX write more instructions, probably using at_exit
  config.vm.provision "shell", privileged: false, inline: <<-EOF
    echo "Review Board: http://localhost:#{configs['REVIEWBOARD_PORT']}/"
    echo "Bugzilla: http://localhost:#{configs['BUGZILLA_PORT']}/"
  EOF
end
