resource "aws_s3_bucket" "bucket" {
  bucket = "super-duper-crazy-bucket"
  acl    = "private"

  tags = {
    Name        = "super-duper-crazy-bucket"
  }
}
