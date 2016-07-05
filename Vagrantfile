# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  # Allow local machines to view the VM
  config.vm.network "private_network", ip: "192.168.2.2"

  config.vm.provision "ansible" do |ansible|

  ansible.groups = {
    "database" => ["default"],
    "search" => ["default"],
    "pubtool" => ["default"],
    "frontend" => ["default"]
  }

    ansible.playbook = "deploy/deploy_dev.yml"
  end

  config.vm.provider :virtualbox do |vb|
    config.vm.box = "ubuntu/xenial64"
    # boot headless (or make true to get a display)
    vb.gui = false
    # Virtualbox Custom CPU count:
    vb.customize ["modifyvm", :id, "--name", "dgu2_vm"]
    vb.customize ["modifyvm", :id, "--memory", "8192"]
    vb.customize ["modifyvm", :id, "--cpus", "8"]
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
    config.vm.synced_folder "src", "/home/ubuntu/apps"
  end


end
