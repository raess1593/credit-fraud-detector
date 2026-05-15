resource "aws_ecr_repository" "api" {
  name = "${local.name_prefix}-api"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-api"
  })
}

resource "aws_ecr_repository" "mlflow" {
  name = "${local.name_prefix}-mlflow"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-mlflow"
  })
}

resource "aws_ecr_repository" "training" {
  name = "${local.name_prefix}-training"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-training"
  })
}
