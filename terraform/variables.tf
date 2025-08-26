variable "rg_name" {
  type        = string
  description = "Ressource group name"
}

variable "location" {
  type        = string
  description = "Ressources location"
}

variable "azure_aad_application_owner_object_id" {
  type        = string
  description = "The azure aad application owner object id"
}

variable "tenant_id" {
  type        = string
  description = "tenant id"

}