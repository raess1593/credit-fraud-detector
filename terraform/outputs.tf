output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "private_subnet_ids" {
  description = "Private subnet IDs"
  value       = aws_subnet.private[*].id
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "rds_endpoint" {
  description = "RDS endpoint address"
  value       = aws_db_instance.mlflow.address
}

output "mlflow_artifacts_bucket" {
  description = "S3 bucket for MLflow artifacts"
  value       = aws_s3_bucket.mlflow_artifacts.bucket
}

output "dvc_bucket" {
  description = "S3 bucket for DVC data"
  value       = aws_s3_bucket.dvc_data.bucket
}

output "alb_internal_dns" {
  description = "Internal ALB DNS name"
  value       = aws_lb.internal.dns_name
}

output "ecr_api_repo" {
  description = "ECR repository for API"
  value       = aws_ecr_repository.api.repository_url
}

output "ecr_mlflow_repo" {
  description = "ECR repository for MLflow"
  value       = aws_ecr_repository.mlflow.repository_url
}

output "ecr_training_repo" {
  description = "ECR repository for training"
  value       = aws_ecr_repository.training.repository_url
}

output "training_task_definition" {
  description = "Training task definition ARN"
  value       = aws_ecs_task_definition.training.arn
}
