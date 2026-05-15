resource "aws_ecr_repository" "api" {
  name = "${local.name_prefix}-api"
  force_delete = true

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-api"
  })
}

resource "aws_ecr_repository" "mlflow" {
  name = "${local.name_prefix}-mlflow"
  force_delete = true

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-mlflow"
  })
}

resource "aws_ecr_repository" "training" {
  name = "${local.name_prefix}-training"
  force_delete = true

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-training"
  })
}
