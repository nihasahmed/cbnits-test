variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
  default     = "myResourceGroup"
}

variable "location" {
  description = "The location where resources will be deployed"
  type        = string
  default     = "eastus"
}

variable "vnet_name" {
  description = "The name of the virtual network"
  type        = string
  default     = "myVNet"
}

variable "vnet_address_space" {
  description = "The address space for the virtual network"
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_name" {
  description = "The name of the subnet"
  type        = string
  default     = "mySubnet"
}

variable "subnet_address_prefix" {
  description = "The address prefix for the subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "container_group_name" {
  description = "The name of the container group"
  type        = string
  default     = "myContainerGroup"
}

variable "container_name" {
  description = "The name of the container"
  type        = string
  default     = "myContainer"
}

variable "image_name" {
  description = "The name of the Docker image"
  type        = string
  default     = "your_dockerhub_username/your_image_name:tag"
}

variable "cpu_cores" {
  description = "The number of CPU cores to allocate to the container"
  type        = number
  default     = 1
}

variable "memory_size" {
  description = "The amount of memory to allocate to the container in GB"
  type        = number
  default     = 1.5
}

variable "container_port" {
  description = "The port on which the container will listen"
  type        = number
  default     = 5000
}

variable "auth0_domain" {
  description = "Auth0 domain"
  type        = string
}

variable "auth0_client_id" {
  description = "Auth0 client ID"
  type        = string
}

variable "auth0_client_secret" {
  description = "Auth0 client secret"
  type        = string
}
