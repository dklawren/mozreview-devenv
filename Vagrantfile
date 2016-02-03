Vagrant.require_version ">= 1.7.0"

require 'yaml'
current_dir    = File.dirname(File.expand_path(__FILE__))
configs        = YAML.load_file("#{current_dir}/config.yml")

Vagrant.configure(2) do |config|
  config.vm.box = "puppetlabs/centos-7.2-64-nocm"
  config.vm.network "private_network", type: "dhcp"

  config.vm.provider "virtualbox" do |v|
    v.name = "mozreview-dev"
    v.memory = 1024
    v.cpus = 2
  end

  config.vm.provider :parallels do |prl, override|
    override.vm.box = "parallels/centos-7.2"
    prl.update_guest_tools = true
    prl.name = "mozreview-dev"
    prl.memory = 1024
    prl.cpus = 2
  end

  config.vm.hostname = "mozreview-dev"
  config.vm.network :forwarded_port, guest: configs['REVIEWBOARD_PORT'], host: configs['REVIEWBOARD_PORT']
  config.vm.network :forwarded_port, guest: configs['BUGZILLA_PORT'], host: configs['BUGZILLA_PORT']
  config.vm.network :forwarded_port, guest: configs['HGWEB_PORT'], host: configs['HGWEB_PORT']
  config.vm.network :forwarded_port, guest: 222, host: configs['SSH_PORT']

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

  config.trigger.after [:up, :provision] do
    unless File.exist?('test-repo')
      info "creating default users"
      run_remote "sh /src/dev/scripts/create-default-users >/dev/null"
      run "./scripts/create-test-repo"
    end
    info "-=-=-=-=-=-=-"
    info "Review Board: http://localhost:#{configs['REVIEWBOARD_PORT']}/"
    info "Bugzilla: http://localhost:#{configs['BUGZILLA_PORT']}/"
    info "HG Web: http://localhost:#{configs['HGWEB_PORT']}/"
    info "Mercurial repository: ./test-repo/"
    info "-=-=-=-=-=-=-"
  end
end
