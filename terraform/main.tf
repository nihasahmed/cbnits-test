provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_container_group" "container_group" {
  name                = var.container_group_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"

  container {
    name   = var.container_name
    image  = var.image_name
    cpu    = var.cpu_cores
    memory = var.memory_size
    ports {
      port     = var.container_port
      protocol = "TCP"
    }
    environment_variables = {
      "AUTH0_DOMAIN"        = var.auth0_domain
      "AUTH0_CLIENT_ID"     = var.auth0_client_id
      "AUTH0_CLIENT_SECRET" = var.auth0_client_secret
    }
  }

  tags = {
    environment = "testing"
  }

}