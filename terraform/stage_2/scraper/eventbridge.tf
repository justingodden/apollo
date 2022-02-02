resource "aws_iam_role" "ecs_events-role" {
  name = "ecs_events"

  assume_role_policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Sid" : "",
          "Effect" : "Allow",
          "Principal" : {
            "Service" : "events.amazonaws.com"
          },
          "Action" : "sts:AssumeRole"
        }
      ]
    }
  )
}

## for step functions
# {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Effect": "Allow",
#             "Action": [
#                 "states:StartExecution"
#             ],
#             "Resource": [
#                 "arn:aws:states:us-east-1:005165627580:stateMachine:MyStateMachine"
#             ]
#         }
#     ]
# }
resource "aws_iam_role_policy" "ecs_events_run_task_with_any_role" {
  name = "ecs_events_run_task_with_any_role"
  role = aws_iam_role.ecs_events-role.id

  policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Effect" : "Allow",
          "Action" : "iam:PassRole",
          "Resource" : "*"
        },
        {
          "Effect" : "Allow",
          "Action" : "ecs:RunTask",
          "Resource" : "${replace(aws_ecs_task_definition.scraper-task-definition.arn, "/:\\d+$/", ":*")}"
        }
      ]
    }
  )
}

resource "aws_cloudwatch_event_rule" "scraper-eventbridge" {
  name                = "apollo-scraper-weekly"
  description         = "Weekly ECS Fargate task for Apollo scraper"
  schedule_expression = "rate(7 days)"
}

resource "aws_cloudwatch_event_target" "scraper-event-target" {
  rule     = aws_cloudwatch_event_rule.scraper-eventbridge.name
  arn      = "arn:aws:ecs:us-east-1:005165627580:cluster/apollo-ecs-cluster-test" # TODO: use output instead of hardcoding
  role_arn = aws_iam_role.ecs_events-role.arn

  ecs_target {
    task_count          = 1
    task_definition_arn = aws_ecs_task_definition.scraper-task-definition.arn
    network_configuration {
      subnets = var.subnet_ids
      #  security_groups = [var.security_group_id]
    }
    launch_type = "FARGATE"
  }
}
