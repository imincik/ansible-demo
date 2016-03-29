# Automated Deployment Demonstration

**This project is for demonstration purposes only. Don't use in production !**

The goal of this project is to demonstrate basic principles of automated
deployment of development and production infrastructure.

**Requirements:**  
* **Linux** or **Mac OSX** - operating system
* **Git**                  - source code storage and versioning
* **Vagrant**              - virtual machines provisioning
* **Ansible**              - infrastructure orchestration


# Basic knowledge
## YAML

A straightforward machine parseable data serialization format designed for human
readability and interaction with scripting languages such as Perl and Python.

## Ansible

Ansible is written in Python and it is using YAML for configuration. It is using
SSH to connect to servers. Ansible executes *playbooks*, which are the
definitions of tasks and environment to execute.  

The goal of a play is to map a group of hosts to some well defined *roles*,
represented by things Ansible calls *tasks*. At a basic level, a task is nothing
more than a call to an Ansible module.  

Whole process of playbook execution must be *idempotent*.


### Tasks

* create PostgreSQL user using 'shell' module (non-idempotent)  
```yaml
- name: Create 'dbuser' account in PostgreSQL db
  shell: createuser dbuser
```

* create PostgreSQL user using 'postgresql_user' module (idempotent)  
```yaml
- name: Create 'dbuser' account in PostgreSQL db
  postgresql_user:
    name: dbuser
    password: dbuser_password
    state: present
```

# install PostgreSQL (idempotent)
```yaml
- name: Install PostgreSQL
  apt:
    pkg: postgresql-9.3
    force: yes
    install_recommends: no
    state: latest
```

### Variables

* variable declaration  
```yaml
DATABASE_USER_NAME: dbuser
DATABASE_USER_PASSWORD: dbuser
```

* variable usage in task  
```yaml
- name: Create 'dbuser' account in PostgreSQL db
  postgresql_user:
    name: "{{ DATABASE_USER_NAME }}"
    password: "{{ DATABASE_USER_PASSWORD }}"
    state: present
```

### Templates (jinja2)

* variables declaration  
```yaml
DEBUG: yes

# list of users
USERS:
  - ivan
  - simon
  - joe
```

* variable usage in template and resulting file produced  
```html+jinja
{% if DEBUG %}
Running in debug mode !
{% endif %}

List of users:
{% for user in USERS %}
  * {{ user }}
{% endfor %}
```
```
Running in debug mode !

List of users:
  * ivan
  * simon
  * joe
```

* template deployment using 'template' module  
```yaml
- name: Configure PostgreSQL access policy
  template:
    src: postgresql/pg_hba.conf.j2
    dest: /etc/postgresql/9.3/main/pg_hba.conf
```

### Handlers

* handler declaration  
```yaml
- name: service postgresql restart
  service:
    name: postgresql
    state: restarted
```

* handler activation  
```yaml
- name: Configure PostgreSQL access policy
  template:
    src: postgresql/pg_hba.conf.j2
    dest: /etc/postgresql/9.3/main/pg_hba.conf
  notify:
    - service postgresql restart
```

### Files
* script deployment  
```yaml
- name: Install db-stats script
  copy:
    src: static/db-stats/db-stats.py
    dest: /opt/db-stats.py
```

### Roles

* **role** - collection of tasks, templates, handlers and variables creating
             usually one service. Roles can be reusable !  

* **playbook** - collection of selected roles  
```yaml
- hosts: db
  roles:
    - { role: basic }
    - { role: service-database }
```

### Directories structure

```
├── group_vars
│   └── all
├── host_vars
│   └── README
├── roles

│   ├── basic
│   │   ├── tasks
│   │   │   └── main.yml
│   │   └── templates
│   │       └── apt
│   │           └── sources.list.j2

│   ├── service-database
│   │   ├── handlers
│   │   │   └── main.yml
│   │   ├── tasks
│   │   │   └── main.yml
│   │   └── templates
│   │       └── postgresql
│   │           ├── pg_hba.conf.j2
│   │           └── pg_ident.conf.j2

│   ├── service-load-balancer
│   │   ├── handlers
│   │   │   └── main.yml
│   │   ├── tasks
│   │   │   └── main.yml
│   │   └── templates
│   │       └── haproxy
│   │           ├── haproxy.cfg.j2
│   │           └── haproxy.j2

│   ├── service-web
│       ├── files
│       │   └── static
│       │       └── db-stats
│       │           └── db-stats.py
│       ├── tasks
│       │   └── main.yml
│       ├── templates
│       │   ├── db-stats
│       │   │   └── db-stats.conf.j2
│       │   └── init
│       │       └── rc.local.j2
│       └── vars
│           └── main.yml

├── db-deploy.yml
├── db-test.yml
├── lb-deploy.yml
├── lb-test.yml
├── web-deploy.yml
└── web-test.yml
```

### Tasks delegation


## Vagrant
### Vagrant file
* configuration file written in Ruby  
```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "base"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   sudo apt-get update
  #   sudo apt-get install -y apache2
  # SHELL
end
```

### Commands
### Shared directory


# Infrastructure
## Services

List of implemented services:  
* db  - database service
* web - web service (simple app returning some data from db)
* lb  - load balancer service on top of the web service

## Ports

List of active TCP ports forwarded from VMs to host machine:  
* db  - PostgreSQL          - vm: 5432, host: 15432
* lb  - load balancer stats - vm: 8100, host: 18100
* lb  - web service         - vm: 80,   host: 10080
* web - web service         - vm: 8000, host: 18000



# Quick Start
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
$ sudo apt-get install ansible
```

### VirtualBox

* install Dynamic Kernel Module Support Framework  
```
$ sudo apt-get install dkms
```

* download and install VirtualBox 5 package from
  https://www.virtualbox.org/wiki/Downloads  

* install missing dependencies  
```
$ sudo apt-get -f install
```

### Vagrant

* download and install latest Vagrant package from
  http://www.vagrantup.com/downloads.html  

* install missing dependencies  
```
$ sudo apt-get -f install
```


## Deployment

* clone source code from Git  
```
$ git clone <GIT-REPOSITORY-URL>
```

* start infrastructure in virtual machines  
```
$ vagrant up
```

* check infrastructure status  
```
$ vagrant status
```

* perform update  
```
$ git pull
$ vagrant provision
```

* connect to VM  
```
$ vagrant ssh <VM-NAME>
```

* shutdown whole infrastructure  
```
$ vagrant halt
```
