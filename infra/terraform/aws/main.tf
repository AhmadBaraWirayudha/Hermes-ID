terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" { region = var.aws_region }

# Skeleton only: wire to your registry image and networking standards.
resource "aws_s3_bucket" "artifacts" {
  bucket_prefix = "indomarket-artifacts-"
}

resource "aws_ecr_repository" "app" {
  name = "indomarket-insight"
}

output "ecr_repository_url" { value = aws_ecr_repository.app.repository_url }
output "artifact_bucket" { value = aws_s3_bucket.artifacts.bucket }
