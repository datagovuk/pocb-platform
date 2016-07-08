
# Setup

## Building the development environment

To build the development environment, you will need to have the following 
software installed:

* Virtualbox (recent)
* Vagrant (vagrantup.com) v1.8.4+
* Ansible (pip install ansible) v2.1+

Before you start, you should add a couple of entries to the ```/etc/hosts``` on your dev 
machine if you have both services on a single box and want to access them via nginx.
You should add:

```
192.168.2.2  pubtool.local
192.168.2.2  frontend.local
```

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

## Starting pubtool for development

```bash
cd ~/apps/
./pubtool-run.sh
# Go to http://192.168.2.2:5001/manage in your browser
```

## Starting frontend for development

```bash
cd ~/apps/
./frontend-run.sh
# Go to http://192.168.2.2:5002/ in your browser
```

# Data 

The data for the objects used by the pubtool are help in MongoDB and can be found in the relevant collections (documented in the table below). When data is referenced from one collection to another, this is done by the object_id but should be minimal.

| Collection  |  Contains |
|---|---|
| publishers | Details about the publishing organisations that interact with the pubtool |
| datasets  |   |
| users  |   |



