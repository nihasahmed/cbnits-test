output "container_group_name" {
  description = "The name of the container group"
  value       = azurerm_container_group.container_group.name
}

output "container_ip_address" {
  description = "The IP address of the container"
  value       = azurerm_container_group.container_group.ip_address
}
