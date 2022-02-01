resource "aws_iam_role" "scraper-task-role" {
  name = "apollo-scraper-ecs-task-role"

  assume_role_policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Action" : "sts:AssumeRole",
          "Principal" : {
            "Service" : "ecs-tasks.amazonaws.com"
          },
          "Effect" : "Allow",
          "Sid" : ""
        }
      ]
    }
  )
}

resource "aws_iam_role" "scraper-task-execution-role" {
  name = "apollo-scraper-ecs-task-execution-role"

  assume_role_policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Action" : "sts:AssumeRole",
          "Principal" : {
            "Service" : "ecs-tasks.amazonaws.com"
          },
          "Effect" : "Allow",
          "Sid" : ""
        }
      ]
    }
  )
}

resource "aws_iam_policy" "scraper-task-policy" {
  name        = "scraper-task-policy"
  description = "scraper-task-policy"

  policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Action" : [
            "secretsmanager:*",
            "cloudformation:CreateChangeSet",
            "cloudformation:DescribeChangeSet",
            "cloudformation:DescribeStackResource",
            "cloudformation:DescribeStacks",
            "cloudformation:ExecuteChangeSet",
            "ec2:DescribeSecurityGroups",
            "ec2:DescribeSubnets",
            "ec2:DescribeVpcs",
            "kms:DescribeKey",
            "kms:ListAliases",
            "kms:ListKeys",
            "lambda:ListFunctions",
            "rds:DescribeDBClusters",
            "rds:DescribeDBInstances",
            "redshift:DescribeClusters",
            "tag:GetResources",
            "dbqms:CreateFavoriteQuery",
            "dbqms:DescribeFavoriteQueries",
            "dbqms:UpdateFavoriteQuery",
            "dbqms:DeleteFavoriteQueries",
            "dbqms:GetQueryString",
            "dbqms:CreateQueryHistory",
            "dbqms:DescribeQueryHistory",
            "dbqms:UpdateQueryHistory",
            "dbqms:DeleteQueryHistory",
            "rds-data:ExecuteSql",
            "rds-data:ExecuteStatement",
            "rds-data:BatchExecuteStatement",
            "rds-data:BeginTransaction",
            "rds-data:CommitTransaction",
            "rds-data:RollbackTransaction",
            "secretsmanager:CreateSecret",
            "secretsmanager:ListSecrets",
            "secretsmanager:GetRandomPassword"
          ],
          "Effect" : "Allow",
          "Resource" : "*"
        },
        {
          "Action" : [
            "lambda:AddPermission",
            "lambda:CreateFunction",
            "lambda:GetFunction",
            "lambda:InvokeFunction",
            "lambda:UpdateFunctionConfiguration"
          ],
          "Effect" : "Allow",
          "Resource" : "arn:aws:lambda:*:*:function:SecretsManager*"
        },
        {
          "Action" : [
            "serverlessrepo:CreateCloudFormationChangeSet",
            "serverlessrepo:GetApplication"
          ],
          "Effect" : "Allow",
          "Resource" : "arn:aws:serverlessrepo:*:*:applications/SecretsManager*"
        },
        {
          "Action" : [
            "s3:GetObject"
          ],
          "Effect" : "Allow",
          "Resource" : [
            "arn:aws:s3:::awsserverlessrepo-changesets*",
            "arn:aws:s3:::secrets-manager-rotation-apps-*/*"
          ]
        },
        {
          "Sid" : "SecretsManagerDbCredentialsAccess",
          "Effect" : "Allow",
          "Action" : [
            "secretsmanager:GetSecretValue",
            "secretsmanager:PutResourcePolicy",
            "secretsmanager:PutSecretValue",
            "secretsmanager:DeleteSecret",
            "secretsmanager:DescribeSecret",
            "secretsmanager:TagResource"
          ],
          "Resource" : "arn:aws:secretsmanager:*:*:secret:rds-db-credentials/*"
        }
      ]
    }
  )
}

resource "aws_iam_policy" "scraper-task-execution-policy" {
  name        = "scraper-task-execution-policy"
  description = "scraper-task-execution-policy"

  policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Effect" : "Allow",
          "Action" : [
            "ecr:GetAuthorizationToken",
            "ecr:BatchCheckLayerAvailability",
            "ecr:GetDownloadUrlForLayer",
            "ecr:BatchGetImage",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
          ],
          "Resource" : "*"
        }
      ]
    }
  )
}

resource "aws_iam_role_policy_attachment" "scraper-task-role-policy-attachment" {
  role       = aws_iam_role.scraper-task-role.name
  policy_arn = aws_iam_policy.scraper-task-policy.arn
}

resource "aws_iam_role_policy_attachment" "scraper-task-execution-role-policy-attachment" {
  role       = aws_iam_role.scraper-task-execution-role.name
  policy_arn = aws_iam_policy.scraper-task-execution-policy.arn
}
