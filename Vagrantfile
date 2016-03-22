# -*- mode: ruby -*-
# vi: set ft=ruby :

#
### CONFIGURATION SECTION
#

Vagrant.require_version ">= 1.7.0"

BOX = "trusty-canonical"
BOX_URL = "http://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-i386-vagrant-disk1.box"

SERVERS = {
    # database
    "db" => {
        "host_number" => "10",
        "memory" => "512",
        "ports" => [
            ["5432", "15432"],
       ]
    },
    # load balancer
    "lb" => {
       "host_number" => "20",
       "memory" => "512",
        "ports" => [
            ["8100", "18100"],
            ["80", "10080"],
       ]
    },
    # web service 1
    "web_1" => {
        "host_number" => "11",
        "memory" => "512",
        "ports" => [
            ["8000", "18000"],
       ]
    },
    # web service 2
    "web_2" => {
        "host_number" => "12",
        "memory" => "512",
        "ports" => [
            ["8000", "18000"],
       ]
    }
}


#
### DON'T CHANGE ANYTHING UNDER THIS LINE
#

Vagrant.configure(2) do |config|

    config.vm.box = BOX
    config.vm.box_url = BOX_URL

    config.ssh.forward_agent = true
    config.vm.synced_folder '.', '/vagrant'


    # loop over all configured servers
    SERVERS.each do | name, cfg|
        config.vm.define name do |server|
            sname = name.gsub(/_.*/, "")  # server name without number

            # IP address
            server.vm.network "private_network",
                ip: "172.20.20" + "." + cfg["host_number"]

            # hostname
            server.vm.hostname = sname

            # ports forwarding
            cfg["ports"].each do | port |
                server.vm.network "forwarded_port",
                    guest: port[0],
                    host: port[1],
                    auto_correct: true
            end

            ### DEPLOYMENT
            server.vm.provision "deploy", type: "ansible" do |ansible|
                ansible.playbook = "provision/" + sname + "-deploy.yml"
                ansible.verbose = "vv"
            end

            ### TEST
            server.vm.provision "test", type: "ansible" do |ansible|
                ansible.playbook = "provision/" + sname + "-test.yml"
                ansible.verbose = "vv"
            end

            ### PROVIDERS CONFIGURATION
            # VirtualBox
            server.vm.provider "virtualbox" do |vb, override|
                vb.customize ["modifyvm", :id, "--memory", cfg["memory"]]
                vb.customize ["modifyvm", :id, "--nictype1", "virtio"]
                vb.customize ["modifyvm", :id, "--nictype2", "virtio"]
#               vb.gui = true
            end
        end
    end
end

# vim: set ts=8 sts=4 sw=4 et:
