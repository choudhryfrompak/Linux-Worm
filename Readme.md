
# SETTING UP ENVIRONMENT TO TEST WORM:

## Cretae containers by running 
`docker compuse up -d`

## Check wether hosts are created or not
`docker ps`
- you should see 4 host containers.

## on local machine:
`ssh-keygen -t rsa`
- (press enter 3-4 times)
` cat ~/.ssh/id_rsa.pub`
copy that key and store it safely.

## execute shell into host(container)
`docker exec -it <container_name> /bin/sh`
## replace container name with hostnames

## On all host containers execute these commands.

`apk add openssh-server`
`apk add openssh-client`
`echo "Port 22" > /etc/ssh/sshd_config`
`echo "PermitRootLogin yes" >> /etc/ssh/sshd_config`
`echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config`
`ssh-keygen -A`
`mkdir -p ~/.ssh`
`echo "<ssh key from host>" >> ~/.ssh/authorized_keys`

## replace <ssh key from host> with the key you saved earlier.
`chmod 700 ~/.ssh`
`chmod 600 ~/.ssh/authorized_keys`
`/usr/sbin/sshd`
`exit`
## Do this on all 4 hosts

## now paswordless ssh is enabled
we can use our script now


# TESTING WORM:


`cd src`
`pip install paramiko`
`python worm.py "<command to execute> <ip addresses of host seperated by spaces>`
# example :
`python worm.py "hostname" 172.19.0.4 172.19.0.2 172.19.0.3 172.19.0.1`
you will get your desired output 

_________________________________________________________________________________________________________________________
=================================================
SETTING UP ENVIRONMENT FOR INTERNAL HOST TESING :
=================================================

# just add firewall rules using UFW on the local host and try the script.
# commands:
apk add ufw
ufw allow from <enter host ip that you want to allow> to any port 22
# for rejecting hosts:
ufw reject from <enter host ip that you want to allow> to any port 22


