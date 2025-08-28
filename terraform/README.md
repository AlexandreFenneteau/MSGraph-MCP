```shell
terraform init
terraform plan -var-file="dev.tfvars" -out="dev.tfplan"
terraform apply "dev.tfplan"
```

To retrieve a sensitive output (password):
```shell
terraform output azure_aad_app_password
```