resource "aws_s3_bucket" "frontend-bucket" {
  bucket = "apollo-watch-pricer"
  acl    = "private"

  website {
    index_document = "index.html"
  }
}

resource "aws_s3_bucket_ownership_controls" "ownership-controls" {
  bucket = aws_s3_bucket.frontend-bucket.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}
