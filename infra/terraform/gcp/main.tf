terraform {
  required_version = ">= 1.6.0"
  required_providers {
    google = { source = "hashicorp/google", version = "~> 5.0" }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = "indomarket-insight"
  format        = "DOCKER"
}

resource "google_storage_bucket" "artifacts" {
  name          = "${var.project_id}-indomarket-artifacts"
  location      = var.region
  force_destroy = false
}

output "artifact_registry" { value = google_artifact_registry_repository.repo.name }
output "bucket" { value = google_storage_bucket.artifacts.name }
