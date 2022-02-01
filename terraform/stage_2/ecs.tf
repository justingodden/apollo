resource "aws_ecs_cluster" "ecs-cluster" {
  name = "apollo-ecs-cluster-test"
}

resource "aws_ecs_cluster_capacity_providers" "ecs-cluster-capacity-providers" {
  cluster_name = aws_ecs_cluster.ecs-cluster.name

  capacity_providers = ["FARGATE", "FARGATE_SPOT"]
}
