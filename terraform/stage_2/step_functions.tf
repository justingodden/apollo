# # create state machine role that can start fargate tasks:
# {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Effect": "Allow",
#             "Action": [
#                 "xray:PutTraceSegments",
#                 "xray:PutTelemetryRecords",
#                 "xray:GetSamplingRules",
#                 "xray:GetSamplingTargets"
#             ],
#             "Resource": [
#                 "*"
#             ]
#         }
#     ]
# }

# {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Effect": "Allow",
#             "Action": [
#                 "ecs:RunTask"
#             ],
#             "Resource": [
#                 "arn:aws:ecs:us-east-1:005165627580:task-definition/apollo-scraper-task-definition-test:3",
#                 "arn:aws:ecs:us-east-1:005165627580:task-definition/apollo-modeller-task-definition:4"
#             ]
#         }
#     ]
# }

# # create state machine:
# {
#   "Comment": "A description of my state machine",
#   "StartAt": "ECS RunTask scraper",
#   "States": {
#     "ECS RunTask scraper": {
#       "Type": "Task",
#       "Resource": "arn:aws:states:::ecs:runTask",
#       "Parameters": {
#         "LaunchType": "FARGATE",
#         "Cluster": "arn:aws:ecs:us-east-1:005165627580:cluster/apollo-ecs-cluster-test",
#         "TaskDefinition": "arn:aws:ecs:us-east-1:005165627580:task-definition/apollo-scraper-task-definition-test:3"
#       },
#       "Next": "ECS RunTask modeller"
#     },
#     "ECS RunTask modeller": {
#       "Type": "Task",
#       "Resource": "arn:aws:states:::ecs:runTask",
#       "Parameters": {
#         "LaunchType": "FARGATE",
#         "Cluster": "arn:aws:ecs:us-east-1:005165627580:cluster/apollo-ecs-cluster-test",
#         "TaskDefinition": "arn:aws:ecs:us-east-1:005165627580:task-definition/apollo-modeller-task-definition:4"
#       },
#       "End": true
#     }
#   }
# }
