# credit-fraud-detector

🚀 **Credit Fraud Detector** is an end-to-end ML system with Infrastructure as Code (IaC). It provisions AWS infrastructure, trains models with MLflow, promotes the best model to Production, and serves predictions via a FastAPI service.

---

## 🧭 Project Goals
- **IaC-first**: all infrastructure is reproducible with Terraform.
- **Production-like flow**: model registry, promotion, and controlled deployment.
- **Security-focused**: least privilege IAM, private networking, and Secrets Manager for DB credentials.
- **Scalable deployment**: containers on ECS Fargate with internal ALB.

---

## 🧱 Architecture Overview
1) **Training** runs in a container and logs runs/metrics to MLflow.
2) **MLflow Tracking Server** stores:
	- Metadata in **RDS Postgres**
	- Artifacts (models) in **S3**
3) **Model Registry** handles promotion to **Production**.
4) **API** loads **Production** model only and serves predictions.

---

## 🗺️ AWS Components (IaC)
- **VPC + Subnets + NAT + Security Groups**
- **S3** for MLflow artifacts
- **RDS Postgres** for MLflow metadata
- **ECR** for container images
- **ECS Fargate** for MLflow and API services
- **Internal ALB** for service routing

---

## 🧪 Model Promotion Logic
The training pipeline registers a new model version in MLflow Registry and:
- Promotes to **Production** **only if** it beats current Production `test_f1` and meets threshold.
- Otherwise it goes to **Staging** or is **Rejected**.

The API always loads:
```
models:/<model_name>/Production
```

---

## 🔐 Security Notes
- **No secrets in Git**: `.env` and `*.tfvars` are ignored.
- **RDS password** is managed by **AWS Secrets Manager**.
- **ECS task role** has least-privilege access to S3 and Secrets.
- **Internal ALB** means API/MLflow are only reachable inside the VPC.

---

## ✅ Prerequisites
- AWS CLI configured
- Docker Desktop (or Docker Engine)
- Terraform installed

---

## ⚙️ Local Config (non-committed)
Create `terraform/dev.tfvars` from `terraform/dev.tfvars.example`:
- `artifacts_bucket_name`
- `api_image`
- `mlflow_image`

---

## 🚢 Deploy (Manual)
1) **Build & push images**
```
AWS_ACCOUNT_ID=<your-account-id>
AWS_REGION=us-east-1

aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

docker build -t cfd-api -f Dockerfile.api .
docker tag cfd-api:latest "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/credit-fraud-detector-dev-api:v1"
docker push "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/credit-fraud-detector-dev-api:v1"

docker build -t cfd-train -f Dockerfile.train .
docker tag cfd-train:latest "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/credit-fraud-detector-dev-training:v1"
docker push "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/credit-fraud-detector-dev-training:v1"
```

2) **Apply Terraform**
```
cd terraform
terraform init
terraform apply -var-file=dev.tfvars
```

---

## ⛔ Stop (Zero Cost)
```
cd terraform
terraform destroy -var-file=dev.tfvars
```

If destroy fails because ECR repos are not empty, delete images or keep `force_delete = true` in `terraform/ecr.tf`.

---

## 🤖 CI/CD
`main.yml` orchestrates lint, tests, and deploy:
- Lint + Tests on push/PR to `main`
- Deploy on push to `main` (or manual dispatch)

**Required GitHub Secrets:**
- `AWS_ROLE_ARN`
- `AWS_REGION`
- `AWS_ACCOUNT_ID`
- `TF_ARTIFACTS_BUCKET`

---

## ✅ Verification Checklist
1) ECS services running (API + MLflow)
2) CloudWatch logs show successful startup
3) Run training task → new MLflow model version appears
4) Production updates only if `test_f1` improves
5) API responds via internal ALB from inside the VPC

---

## 📦 Repo Structure
- `train.py`: training and promotion logic
- `api/`: FastAPI app
- `src/`: ML utilities (data/model)
- `terraform/`: AWS IaC
- `.github/workflows/`: CI/CD

---

## 🧠 How It Works (End-to-End)
1) **Infra**: Terraform creates VPC, RDS, S3, ECS, ALB.
2) **Training**: runs in a container, logs to MLflow.
3) **Promotion**: MLflow Registry controls Production stage.
4) **Serving**: API loads Production model only.
5) **Ops**: CI/CD builds images and applies Terraform.