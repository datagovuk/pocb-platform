

# Using the vagrantfile

In order to use the Vagrantfile to boot a Virtualbox
VM you will need to ensure you are using Vagrant 1.8.4 
or greater and have Ansible 2.1+ installed.

WORKAROUND: The Ubuntu Xenial image isn't quite complete, so there 
is a slight issue in bringing up the VM where it needs 
to be multi-step. This will be unnecessary when Ubuntu fix their
cloud image.

```
vagrant up
# Previous step will show an error, but ...
vagrant ssh
sudo apt-get --no-install-recommends install virtualbox-guest-utils
exit
vagrant reload
```

