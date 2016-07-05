
# Setup

## Building the development environment

To build the development environment, you will need to have the following 
software installed:

* Virtualbox (recent)
* Vagrant (vagrantup.com) v1.8.4+
* Ansible (pip install ansible) v2.1+

Due to a (temporary) problem with Ubuntu's Xenial image, the setup is 
currently a 2 phase setup, but only needs to be completed once. When 
the image is fixed, we can fix the process.

```bash
vagrant up
# Previous step will show an error, but ...
vagrant ssh
sudo apt-get --no-install-recommends install virtualbox-guest-utils
exit
vagrant reload
```

## Activating the virtual environments

Each app (frontend and pubtool) has its own virtualenv in ```/usr/lib/dgu/{pubtool,frontend}```. The appropriate virtualenv should be activated before you work on it, this might look like 

```
. /usr/lib/dgu/frontend/bin/activate
```