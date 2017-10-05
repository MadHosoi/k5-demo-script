
# Connect via SSH

ssh -i Secrets/cnets-mdiego.pem ubuntu@<externalip>

# Script with bash commands

sudo sh -c "echo <internalip> <hostname> >> /etc/hosts"

# Install Docker

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
apt-cache policy docker-ce
sudo apt-get install -y docker-ce
sudo usermod -aG docker ubuntu

sudo docker run -d -p 80:8080 madhosoi/k5websample:v.1.0