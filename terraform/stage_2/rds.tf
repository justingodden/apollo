resource "aws_db_subnet_group" "apollo-subnet-group" {
  name       = "apollo-subnet-group"
  subnet_ids = [aws_subnet.apollo-public-subnet-1.id, aws_subnet.apollo-public-subnet-2.id]

  tags = {
    Name = "DB subnet group"
  }
}

resource "aws_db_instance" "rds-mysql" {
  identifier           = "apollo-rds-test"
  availability_zone    = "us-east-1a"
  storage_type         = "gp2"
  allocated_storage    = 20
  engine               = "mysql"
  name                 = "apollo"
  engine_version       = "8.0"
  instance_class       = "db.t2.micro"
  db_subnet_group_name = aws_db_subnet_group.apollo-subnet-group.name
  username             = "admin"
  password             = random_password.password.result
  publicly_accessible  = true
  skip_final_snapshot  = true
}

resource "aws_secretsmanager_secret" "apollo-secrets-manager" {
  name        = "apollo-rds-secret-test1"
  description = "Access to MySql db for Apollo project"
}

resource "aws_secretsmanager_secret_version" "apollo-secrets" {
  secret_id = aws_secretsmanager_secret.apollo-secrets-manager.id
  secret_string = jsonencode({
    username : "admin",
    password : random_password.password.result
  })
}

resource "random_password" "password" {
  length           = 16
  special          = true
  override_special = "_%@"
}
