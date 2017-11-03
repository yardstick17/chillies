# chiles_recipe

## Install Docker
```bash
sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo apt-get install docker-ce
sudo docker run hello-world
```

## To run on standalone
 ```bash
bash run.sh standalone # Make sure workers are running
```


## To run on Cluster mode. Used docker based cluster addition and running on master container
 ```bash
bash run.sh cluster # Make sure related filepaths available in docker container
```
