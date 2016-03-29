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
```
- name: Create 'dbuser' account in PostgreSQL db
  postgresql_user:
    name: dbuser
    password: dbuser_password
    state: present
```

# install PostgreSQL (idempotent)
```
- name: Install PostgreSQL
  apt:
    pkg: postgresql-9.3
    force: yes
    install_recommends: no
    state: latest
```

### Variables

* variable declaration  
```
DATABASE_USER_NAME: dbuser
DATABASE_USER_PASSWORD: dbuser
```

* variable usage in task  
```
- name: Create 'dbuser' account in PostgreSQL db
  postgresql_user:
    name: "{{ DATABASE_USER_NAME }}"
    password: "{{ DATABASE_USER_PASSWORD }}"
    state: present
```

### Templates (jinja2)

* variables declaration  
```
DEBUG: yes

# list of users
USERS:
  - ivan
  - simon
  - joe
```

* variable usage in template and resulting file produced  
```
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
```
- name: Configure PostgreSQL access policy
  template:
    src: postgresql/pg_hba.conf.j2
    dest: /etc/postgresql/9.3/main/pg_hba.conf
```

### Handlers

* handler declaration  
```
- name: service postgresql restart
  service:
    name: postgresql
    state: restarted
```

* handler activation  
```
- name: Configure PostgreSQL access policy
  template:
    src: postgresql/pg_hba.conf.j2
    dest: /etc/postgresql/9.3/main/pg_hba.conf
  notify:
    - service postgresql restart
```

### Roles

### Ansible directories structure

### Tasks delegation


## Vagrant
### Vagrant file
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
