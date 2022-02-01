terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }

  backend "s3" {
    bucket = "jg-s3-terraform-state-files"
    key    = "apollo-stage-2/terraform.tfstate"
    region = "us-east-1"
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

module "scraper" {
  source     = "./scraper"
  subnet_ids = [aws_subnet.apollo-public-subnet-1.id, aws_subnet.apollo-public-subnet-2.id]
}
