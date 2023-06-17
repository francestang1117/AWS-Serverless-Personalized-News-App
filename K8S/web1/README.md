# Initialize Terraform 
```
terraform init
```
# Set the GOOGLE_PROJECT environment varible
```
export GOOGLE_PROJECT=csci-5409-s23-k8s
```
# Provision GKE cluster
```
terraform apply
```
# Install kubectl
```
gcloud components install kubectl
```
# Install gke-gcloud-auth-plugin
```
gcloud components install gke-gcloud-auth-plugin
```
# Check version
```
gke-gcloud-auth-plugin --version
```
# Update kubectl configuration
```
gcloud container clusters get-credentials $(terraform output -raw \
k8s_cluste_name) --region us-central1
```
# Verify the configuration
```
kubectl get namespaces
```
