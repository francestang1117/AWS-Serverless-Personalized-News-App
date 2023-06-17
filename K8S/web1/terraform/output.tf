output "k8s_cluste_name" {
    value = google_container_cluster.gke.name
    description = "GKE Cluster name"
}

output "k8s_cluste_host" {
    value = google_container_cluster.gke.endpoint
    description = "GKE Cluster host"
}