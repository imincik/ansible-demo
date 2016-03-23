# Automated Deployment Demonstration

**This project is for demonstration purposes only. Don't use in production !**

The goal of this project is to demonstrate basic principles of automated
deployment of development and production infrastructure.

**Requirements:**  
* **Linux** or **Mac OSX** operating system
* **Git**     - source code storage and versioning
* **Vagrant** - automated virtual machines provisioning
* **Ansible** - infrastructure orchestration


## Installation instructions - Ubuntu 14.04
### Ansible
* add Ansible repository  
```
$ sudo apt-get install software-properties-common
$ sudo apt-add-repository ppa:ansible/ansible
$ sudo apt-get update
```

* install Ansible  
```
$ sudo apt-get install ansible`
```

### VirtualBox
* add VirtualBox repository signing key  
```
$ wget -q http://download.virtualbox.org/virtualbox/debian/oracle_vbox.asc -O- | sudo apt-key add -
```

* add VirtualBox repository to system  
```
$ sudo sh -c 'echo "deb http://download.virtualbox.org/virtualbox/debian trusty contrib" > /etc/apt/sources.list.d/virtualbox.list'
```

* install Dynamic Kernel Module Support Framework  
```
$ sudo apt-get update && sudo apt-get install dkms
```

* install VirtualBox  
```
$ sudo apt-get install virtualbox-4.3
```

### Vagrant
* remove previously downloaded Vagrant packages  
```
$ rm -vf ~/Downloads/vagrant_*.deb
```

* manually download Vagrant from http://www.vagrantup.com/downloads.html

* install Vagrant  
```
$ sudo dpkg -i ~/Downloads/vagrant_*.deb
$ sudo apt-get -f install
```
