data "aws_iam_policy_document" "events_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "events_invoke_ecs" {
  name               = "${local.name_prefix}-events-ecs"
  assume_role_policy = data.aws_iam_policy_document.events_assume_role.json

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-events-ecs"
  })
}

resource "aws_iam_role_policy" "events_invoke_ecs" {
  name = "${local.name_prefix}-events-ecs"
  role = aws_iam_role.events_invoke_ecs.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["ecs:RunTask"]
        Resource = [aws_ecs_task_definition.training.arn]
      },
      {
        Effect = "Allow"
        Action = ["iam:PassRole"]
        Resource = [
          aws_iam_role.ecs_task.arn,
          aws_iam_role.ecs_task_execution.arn
        ]
      }
    ]
  })
}

resource "aws_cloudwatch_event_rule" "training_schedule" {
  name                = "${local.name_prefix}-training"
  schedule_expression = var.training_schedule_cron

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-training"
  })
}

resource "aws_cloudwatch_event_target" "training_schedule" {
  rule      = aws_cloudwatch_event_rule.training_schedule.name
  target_id = "${local.name_prefix}-training"
  arn       = aws_ecs_cluster.main.arn
  role_arn  = aws_iam_role.events_invoke_ecs.arn

  ecs_target {
    task_definition_arn = aws_ecs_task_definition.training.arn
    launch_type         = "FARGATE"
    platform_version    = "LATEST"

    network_configuration {
      subnets         = aws_subnet.private[*].id
      security_groups = [aws_security_group.ecs_tasks.id]
      assign_public_ip = false
    }
  }
}
