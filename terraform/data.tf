resource "aws_db_subnet_group" "rds" {
  name        = "${local.name_prefix}-rds-subnet-group"
  description = "Private subnets for MLflow RDS"
  subnet_ids  = aws_subnet.private[*].id

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-rds-subnet-group"
  })
}

resource "aws_security_group" "rds" {
  name        = "${local.name_prefix}-rds"
  description = "Allow Postgres from ECS tasks"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_tasks.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-rds"
  })
}

resource "aws_db_instance" "mlflow" {
  identifier             = "${local.name_prefix}-mlflow"
  engine                 = "postgres"
  engine_version         = "15.17"
  instance_class         = var.db_instance_class
  allocated_storage      = var.db_allocated_storage
  db_name                = var.db_name
  username               = var.db_username
  manage_master_user_password = true
  port                   = 5432
  storage_encrypted      = true
  skip_final_snapshot    = true
  publicly_accessible    = false
  db_subnet_group_name   = aws_db_subnet_group.rds.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  tags = merge(local.tags, {
    Name = "${local.name_prefix}-mlflow"
  })
}
