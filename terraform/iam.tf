data "aws_iam_policy_document" "ecs_task_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ecs_task_execution" {
  name               = "${local.name_prefix}-ecs-task-execution"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_assume_role.json

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-ecs-task-execution"
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role" "ecs_task" {
  name               = "${local.name_prefix}-ecs-task"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_assume_role.json

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-ecs-task"
  })
}

data "aws_iam_policy_document" "ecs_task_s3" {
  statement {
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject",
      "s3:ListBucket",
    ]

    resources = [
      aws_s3_bucket.mlflow_artifacts.arn,
      "${aws_s3_bucket.mlflow_artifacts.arn}/*",
    ]
  }
}

data "aws_iam_policy_document" "ecs_task_secrets" {
  statement {
    actions = [
      "secretsmanager:GetSecretValue",
      "secretsmanager:DescribeSecret",
    ]

    resources = [aws_db_instance.mlflow.master_user_secret[0].secret_arn]
  }
}

resource "aws_iam_role_policy" "ecs_task_s3" {
  name   = "${local.name_prefix}-ecs-task-s3"
  role   = aws_iam_role.ecs_task.name
  policy = data.aws_iam_policy_document.ecs_task_s3.json
}

resource "aws_iam_role_policy" "ecs_task_secrets" {
  name   = "${local.name_prefix}-ecs-task-secrets"
  role   = aws_iam_role.ecs_task.name
  policy = data.aws_iam_policy_document.ecs_task_secrets.json
}
