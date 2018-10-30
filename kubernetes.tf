variable "kubernetes_admin_username" {}
variable "kubernetes_admin_ssh_pub_key" {}
variable "kubernetes_client_id" {}
variable "kubernetes_client_secret" {}

resource "azurerm_kubernetes_cluster" "cpdp_aks_cluster" {
  name                = "cpdp-aks-cluster"
  location            = "${azurerm_resource_group.terraformed.location}"
  resource_group_name = "${azurerm_resource_group.terraformed.name}"
  dns_prefix          = "cpdp"

  linux_profile {
    admin_username = "${var.kubernetes_admin_username}"

    ssh_key {
      key_data = "${var.kubernetes_admin_ssh_pub_key}"
    }
  }

  agent_pool_profile {
    name            = "default"
    count           = 4
    vm_size         = "Standard_D2s_v3"
    os_type         = "Linux"
    os_disk_size_gb = 30
  }

  service_principal {
    client_id     = "${var.kubernetes_client_id}"
    client_secret = "${var.kubernetes_client_secret}"
  }
}

output "kube_config" {
    value = "${azurerm_kubernetes_cluster.cpdp_aks_cluster.kube_config_raw}"
}
