resource "azuread_application" "afen-mgp" {
  display_name     = "afen-mgp-app"
  owners           = [var.azure_aad_application_owner_object_id]
  sign_in_audience = "AzureADMyOrg"

  fallback_public_client_enabled = true

  password {
    display_name = "application-secret"
  }

  public_client {
    redirect_uris = [
      "http://localhost",
    ]
  }

  required_resource_access {
    resource_app_id = "00000003-0000-0000-c000-000000000000" # Microsoft Graph
    resource_access {
      id   = "465a38f9-76ea-45b9-9f34-9e8b0d4b0b42" # Calendars.Read
      type = "Scope"
    }
    resource_access {
      id   = "2b9c4092-424d-4249-948d-b43879977640" # Calendars.Read.Shared
      type = "Scope"
    }
    resource_access {
      id   = "64a6cdd6-aab1-4aaf-94b8-3cc8405e90d0" # email
      type = "Scope"
    }
    resource_access {
      id   = "7427e0e9-2fba-42fe-b0c0-848c9e6a8182" # offline_access
      type = "Scope"
    }
    resource_access {
      id   = "37f7f235-527c-4136-accd-4a02d197296e" # openid
      type = "Scope"
    }
    resource_access {
      id   = "14dad69e-099b-42c9-810b-d002981feec1" # profile
      type = "Scope"
    }
  }
}

output "azure_aad_app_password" {
  sensitive = true
  value     = tolist(azuread_application.afen-mgp.password).0.value
}

output "azure_aad_client_id" {
  sensitive = false
  value     = azuread_application.afen-mgp.client_id
}