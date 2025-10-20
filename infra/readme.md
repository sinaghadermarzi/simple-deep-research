


```
gcloud compute instances create pydata \
    --project=np-public-training \
    --zone=us-west1-b \
    --machine-type=e2-custom-2-1024 \
    --tags=pydata \
    --create-disk=auto-delete=yes,boot=yes,device-name=pydata,image=projects/debian-cloud/global/images/debian-12-bookworm-v20250910,mode=rw,size=50,type=pd-balanced 

gcloud compute ssh --zone "us-west1-b" "pydata" --project "np-public-training"

sudo apt-get install docker-compose up


IP_ADDRESS=$(curl -L -4 iprs.fly.dev)

gcloud compute firewall-rules create \
pydata --allow=tcp:6006,tcp:4317,tcp:8080 \
--description="pydata for arize" \
--direction=INGRESS \
--target-tags=pydata \
--project=np-public-training \
--source-ranges="${IP_ADDRESS}"

https://console.cloud.google.com/net-security/firewall-manager/firewall-policies/details/pydata?project=np-public-training&authuser=0&supportedpurview=project
```




```
gcloud kms keyrings create sops --location global --project=np-public-training
gcloud kms keys create sops-key --location global --keyring sops --purpose encryption --project=np-public-training
gcloud kms keys list --location global --keyring sops --project=np-public-training


sops encrypt --gcp-kms projects/np-public-training/locations/global/keyRings/sops/cryptoKeys/sops-key --input-type dotenv .env > .env.sops

sops --input-type dotenv --output-type dotenv --decrypt .env.sops > .env

sops edit .env.sops --input-type dotenv --output-type dotenv 

```



Start
```

gcloud compute ssh --zone "us-west1-b" "pydata" --project "np-public-training"

docker-compose -f docker-compose__arize.yaml

docker-compose build

docker-compose down && docker-compose build && docker-compose up

docker-compose down && docker-compose build && docker-compose up --force-recreate caddy

```