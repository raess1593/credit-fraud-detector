variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name prefix for resources"
  type        = string
  default     = "credit-fraud-detector"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.10.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "Public subnet CIDRs"
  type        = list(string)
  default     = ["10.10.1.0/24", "10.10.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "Private subnet CIDRs"
  type        = list(string)
  default     = ["10.10.11.0/24", "10.10.12.0/24"]
}

variable "db_name" {
  description = "RDS database name"
  type        = string
  default     = "mlflow"
}

variable "db_username" {
  description = "RDS master username"
  type        = string
  default     = "mlflow"
}


variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "RDS allocated storage (GiB)"
  type        = number
  default     = 5
}

variable "artifacts_bucket_name" {
  description = "S3 bucket name for MLflow artifacts (must be globally unique)"
  type        = string
}

variable "api_image" {
  description = "Container image URI for the API service"
  type        = string
  default     = "python:3.10-slim"
}

variable "mlflow_image" {
  description = "Container image URI for the MLflow service"
  type        = string
  default     = "ghcr.io/mlflow/mlflow:v2.11.3"
}

variable "api_cpu" {
  description = "Fargate CPU units for API"
  type        = number
  default     = 256
}

variable "api_memory" {
  description = "Fargate memory (MiB) for API"
  type        = number
  default     = 512
}

variable "mlflow_cpu" {
  description = "Fargate CPU units for MLflow"
  type        = number
  default     = 256
}

variable "mlflow_memory" {
  description = "Fargate memory (MiB) for MLflow"
  type        = number
  default     = 512
}

variable "api_desired_count" {
  description = "Desired task count for API service"
  type        = number
  default     = 1
}

variable "mlflow_desired_count" {
  description = "Desired task count for MLflow service"
  type        = number
  default     = 1
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 14
}
