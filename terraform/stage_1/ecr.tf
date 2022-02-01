resource "aws_ecr_repository" "ecr-scraper" {
  name                 = "apollo-scraper"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}

resource "aws_ecr_lifecycle_policy" "ecr-policy-scraper" {
  repository = aws_ecr_repository.ecr-scraper.name

  policy = <<EOF
{
    "rules": [
        {
            "rulePriority": 1,
            "description": "Delete all untagged images",
            "selection": {
                "tagStatus": "untagged",
                "countType": "imageCountMoreThan",
                "countNumber": 1
            },
            "action": {
                "type": "expire"
            }
        }
    ]
}
EOF
}

resource "aws_ecr_repository" "ecr-modeller" {
  name                 = "apollo-modeller"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}

resource "aws_ecr_lifecycle_policy" "ecr-policy-modeller" {
  repository = aws_ecr_repository.ecr-modeller.name

  policy = <<EOF
{
    "rules": [
        {
            "rulePriority": 1,
            "description": "Delete all untagged images",
            "selection": {
                "tagStatus": "untagged",
                "countType": "imageCountMoreThan",
                "countNumber": 1
            },
            "action": {
                "type": "expire"
            }
        }
    ]
}
EOF
}

resource "aws_ecr_repository" "ecr-inference" {
  name                 = "apollo-inference"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}

resource "aws_ecr_lifecycle_policy" "ecr-policy-inference" {
  repository = aws_ecr_repository.ecr-inference.name

  policy = <<EOF
{
    "rules": [
        {
            "rulePriority": 1,
            "description": "Delete all untagged images",
            "selection": {
                "tagStatus": "untagged",
                "countType": "imageCountMoreThan",
                "countNumber": 1
            },
            "action": {
                "type": "expire"
            }
        }
    ]
}
EOF
}
