variable "project_id" {
    type = string
    description = "project id for cluster"
}

variable "region" {
    type = string
    description = "region for cluster"
}

variable "num_nodes" {
  default     = 3
  description = "number of gke nodes"
}

variable "location" {
    type = list(string)
    description = "zones for cluster node"
}

resource "google_container_cluster" "gke" {
    name = "${var.project_id}-gke"
    location = var.region
    node_locations = var.location

    remove_default_node_pool = true
    initial_node_count = 1
  
}

resource "google_container_node_pool" "gke_nodes" {
    name = "node-pool"
    project = var.project_id
    location = var.region
    cluster = google_container_cluster.gke.name
    node_count = var.num_nodes

    node_config {
        oauth_scopes = [
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/devstorage.read_only",
            "https://www.googleapis.com/auth/logging.write",
            "https://www.googleapis.com/auth/monitoring",
            "https://www.googleapis.com/auth/servicecontrol",
            "https://www.googleapis.com/auth/service.management.readonly",
            "https://www.googleapis.com/auth/trace.append"
        ]
        metadata = {
            disable-legacy-endpoints = "true"
        }

        machine_type = "e2-medium"
        image_type = "COS_CONTAINERD"
        disk_size_gb = 10
        disk_type = "pd-standard"

    }

}