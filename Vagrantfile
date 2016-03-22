# -*- mode: ruby -*-
# vi: set ft=ruby :

# Set APT_PROXY environment variable before provisioning to speed up packages
# installation using Apt proxy.
# Example:
#   $ export APT_PROXY=http://192.168.99.118:3142

Vagrant.require_version ">= 1.7.0"

BOX = "trusty-canonical"
BOX_URL = "http://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-i386-vagrant-disk1.box"

HOSTS = {
    "db" => ["10", "512", "5432", "15432"],
    "lb" => ["20", "512", "1936", "11936"],
    "web_1" => ["11", "512", "8666", "18666"],
    "web_2" => ["12", "512", "8666", "18666"],
}


Vagrant.configure(2) do |config|

    config.vm.box = BOX
    config.vm.box_url = BOX_URL

    config.ssh.forward_agent = true
    config.vm.synced_folder '.', '/vagrant'

    HOSTS.each do | (name, cfg) |
        host_number, memory, port_guest, port_host = cfg

        config.vm.define name do |server|
            sname = name.gsub(/_.*/, "")  # server name without number

            server.vm.network "private_network",
                ip: "172.20.20" + "." + host_number
            server.vm.hostname = sname
            server.vm.network "forwarded_port",
                guest: port_guest,
                host: port_host,
                auto_correct: true

            # provisioning
            server.vm.provision "deployment", type: "ansible" do |ansible|
                ansible.playbook = "provision/" + sname + "-deployment.yml"
                ansible.verbose = "vv"
            end

            # test
            server.vm.provision "test", type: "ansible" do |ansible|
                ansible.playbook = "provision/" + sname + "-test.yml"
                ansible.verbose = "vv"
            end

            # VirtualBox configuration
            server.vm.provider "virtualbox" do |vb, override|
                vb.customize ["modifyvm", :id, "--memory", memory]
                vb.customize ["modifyvm", :id, "--nictype1", "virtio"]
                vb.customize ["modifyvm", :id, "--nictype2", "virtio"]
#               vb.gui = true
            end
        end
    end
end


# vim: set ts=8 sts=4 sw=4 et:
