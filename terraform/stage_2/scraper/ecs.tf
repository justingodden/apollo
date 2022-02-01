resource "aws_ecs_task_definition" "scraper-task-definition" {
  family                   = "apollo-scraper-task-definition-test"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 1024
  memory                   = 2048
  execution_role_arn       = aws_iam_role.scraper-task-execution-role.arn
  task_role_arn            = aws_iam_role.scraper-task-role.arn
  container_definitions = jsonencode([
    {
      name      = "apollo-scraper"
      image     = "005165627580.dkr.ecr.us-east-1.amazonaws.com/apollo-scraper:latest"
      essential = true
      portMappings = [
        {
          protocol      = "tcp"
          containerPort = 80
          hostPort      = 80
        }
      ]
    }
  ])
}
