resource "aws_vpc" "apollo-vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name = "apollo-vpc-test"
  }
}

resource "aws_internet_gateway" "apollo-igw" {
  vpc_id = aws_vpc.apollo-vpc.id

  tags = {
    Name = "apollo-igw-test"
  }
}

resource "aws_route_table" "apollo-route-table" {
  vpc_id = aws_vpc.apollo-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.apollo-igw.id
  }

  tags = {
    Name = "apollo-route-table-test"
  }
}

resource "aws_subnet" "apollo-public-subnet-1" {
  vpc_id            = aws_vpc.apollo-vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "apollo-public-subnet-1-test"
  }
}

resource "aws_subnet" "apollo-public-subnet-2" {
  vpc_id            = aws_vpc.apollo-vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "apollo-public-subnet-2-test"
  }
}

resource "aws_route_table_association" "rta1" {
  subnet_id      = aws_subnet.apollo-public-subnet-1.id
  route_table_id = aws_route_table.apollo-route-table.id
}

resource "aws_route_table_association" "rta2" {
  subnet_id      = aws_subnet.apollo-public-subnet-2.id
  route_table_id = aws_route_table.apollo-route-table.id
}
