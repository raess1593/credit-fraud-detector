.PHONY: lint test train mlflow api terraform destroy

lint:
	black --check src tests api train.py
	isort --check-only src tests api

lint-fix:
	black src tests api train.py
	isort src tests api

test:
	python -m pytest tests/ -v --cov=src --cov-fail-under=60

train:
	python train.py

mlflow:
	mlflow ui

api:
	uvicorn api.api:app --reload

terraform:
	cd terraform && terraform init && terraform apply -var-file=dev.tfvars -auto-approve

destroy:
	cd terraform && terraform destroy -var-file=dev.tfvars -auto-approve