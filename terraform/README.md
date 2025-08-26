```shell
terraform init
terraform plan -var-file="dev.tfvars" -out="dev.tfplan"
terraform apply "dev.tfplan"
```

Pour connaître un output sensitive (password):
```shell
terraform output azure_aad_app_password
```