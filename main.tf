terraform {
  required_providers {
    google = "= 4.66"
  }
  # We store the "state" of our deployment in the following bucket
  # backend "gcs" {
  #   bucket = "stop-search-terraform-repo-state"
  # }
}

provider "google" {
  project = var.project
  region  = var.location
  zone    = var.location
  credentials =file("secrets/stop-search-dev-b95202d28645.json") # will need to change this to work with ci/cd
}

resource "google_storage_bucket" "static" {
 name          = "duckdb-${var.project}"
 location      = var.location
 storage_class = "STANDARD"

 uniform_bucket_level_access = true
}
