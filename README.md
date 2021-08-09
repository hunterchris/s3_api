# s3_api

Flask app who list bucket contents when hitting the / endpoint.

## Contents

- terraform folder: Holds the code to create an S3 bucket. (Default name: super-duper-crazy-bucket)
- docker folder: Holds the app.
- k8s folder: Holds the config to deploy the app to k8s.

### How to build the infra

```
cd terraform
terraform init
terraform plan
terraform apply
```

### How to run the container locally

```
cd docker
docker build -t api .
docker run -p 5000:5000 -d -e AWS_ACCESS_KEY_ID="<Your_Access_Key>" -e AWS_SECRET_ACCESS_KEY="<Your_Secret_Key>" -e BUCKET="<Your_Bucket_Name>" api
curl localhost:5000/
```

### Deployment to k8s

First you need to update the `deployment.yml` with the BUCKET name of choice (Default: super-duper-crazy-bucket)

The deployment expects the k8s secrets `accesskey` and `secretkey` to be present in the cluster, so please have them created before deploying the app:
```
kubectl create secret generic accesskey --from-literal=AWS_ACCESS_KEY_ID=<Your_Access_Key>
kubectl create secret generic secretkey --from-literal=AWS_SECRET_ACCESS_KEY=<Your_Secret_Key>
```

Then you can apply the changes:
```
cd k8s
kubectl apply -f deployment.yml
```

Now you should expose the container, this will create a service and expose the container's port (5000) to the outside:
`kubectl expose deployment s3-api-deployment --type=LoadBalancer --port=5000`

You can now check that the service is running:
Minikube: `minikube service s3-api-deployment` will open a browser with the bucket name and contents or a "Not Found" if the bucket name is invalid.
