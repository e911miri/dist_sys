# A System for Distributed Processing

Learn how to use this system at the [wiki](https://github.com/joshuacook/dist_sys/wiki)

<img src="assets/static/img/dist_sys.png" width=300px">

## Minimal Instructions for Getting It Up and Running on DigitalOcean

### Set Up DigitalOcean Droplet with Docker

1. Set up an account on DigitalOcean
1. Create a new Droplet. 
   1. Choose an Image >> One-Click Apps >> Docker (the latest version available)
   1. Choose a Size. Any size should work. The $5 is sufficient to demonstrate that this works. 
   1. Make sure to add ssh keys. 
   1. Create.
1. SSH into the new droplet. 
    `$ ssh root@#DROPLET_IP#`
1. Install `docker-compose`
    1. `$ sudo apt-get update`
    1. `$ sudo apt-get -y install python-pip`
    1. `$ sudo pip install docker-compose`

### Clone Repo

1. `$ git clone https://github.com/joshuacook/dist_sys.git` (or configure ssh and use an ssh clone #recommended)

### Launch the System

1. `$ cd dist_sys`
1. `$ make`
