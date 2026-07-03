#!/bin/bash
# AWS Setup Script for Energy Dashboard Deployment
# This script creates the necessary AWS resources for GitHub Actions deployment

set -e  # Exit on error

echo "=========================================="
echo "AWS Setup for Energy Dashboard"
echo "=========================================="

# Configuration
AWS_REGION=${1:-us-east-1}
ECR_REPO_NAME="energy-dashboard"
IAM_USER_NAME="github-actions-deploy"

echo ""
echo "Region: $AWS_REGION"
echo "ECR Repository: $ECR_REPO_NAME"
echo "IAM User: $IAM_USER_NAME"
echo ""

# Step 1: Create ECR Repository
echo "Step 1/4: Creating ECR Repository..."
ECR_RESPONSE=$(aws ecr create-repository \
  --repository-name $ECR_REPO_NAME \
  --region $AWS_REGION \
  --query 'repository.repositoryUri' \
  --output text 2>/dev/null || echo "EXISTING")

if [ "$ECR_RESPONSE" = "EXISTING" ]; then
  echo "✓ ECR repository already exists"
  ECR_URI=$(aws ecr describe-repositories \
    --repository-names $ECR_REPO_NAME \
    --region $AWS_REGION \
    --query 'repositories[0].repositoryUri' \
    --output text)
else
  ECR_URI=$ECR_RESPONSE
  echo "✓ ECR repository created: $ECR_URI"
fi

# Step 2: Create IAM User
echo ""
echo "Step 2/4: Creating IAM User..."
aws iam create-user --user-name $IAM_USER_NAME 2>/dev/null && \
  echo "✓ IAM user created: $IAM_USER_NAME" || \
  echo "✓ IAM user already exists: $IAM_USER_NAME"

# Step 3: Attach ECR Policy
echo ""
echo "Step 3/4: Attaching ECR permissions to IAM user..."
aws iam attach-user-policy \
  --user-name $IAM_USER_NAME \
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser && \
  echo "✓ ECR policy attached"

# Step 4: Create and Display Access Keys
echo ""
echo "Step 4/4: Checking for existing access keys..."
ACCESS_KEYS=$(aws iam list-access-keys --user-name $IAM_USER_NAME --query 'AccessKeyMetadata[].AccessKeyId' --output text)

if [ -z "$ACCESS_KEYS" ]; then
  echo "Creating new access key..."
  KEY_RESPONSE=$(aws iam create-access-key --user-name $IAM_USER_NAME)
  ACCESS_KEY_ID=$(echo $KEY_RESPONSE | jq -r '.AccessKey.AccessKeyId')
  SECRET_ACCESS_KEY=$(echo $KEY_RESPONSE | jq -r '.AccessKey.SecretAccessKey')
  echo "✓ Access key created"
else
  echo "Access keys already exist for this user."
  echo "⚠️  To use existing keys, retrieve them from AWS IAM console"
  echo "   (The secret access key is not retrievable after initial creation)"
  ACCESS_KEY_ID=$ACCESS_KEYS
fi

# Display Summary
echo ""
echo "=========================================="
echo "Setup Complete! ✓"
echo "=========================================="
echo ""
echo "📝 Save these values for GitHub Secrets:"
echo ""
echo "ECR_URI:"
echo "  $ECR_URI"
echo ""
echo "AWS_ACCESS_KEY_ID:"
echo "  $ACCESS_KEY_ID"
echo ""
if [ ! -z "$SECRET_ACCESS_KEY" ]; then
  echo "AWS_SECRET_ACCESS_KEY:"
  echo "  $SECRET_ACCESS_KEY"
  echo ""
  echo "⚠️  IMPORTANT: Save the secret key securely! It won't be shown again."
  echo ""
else
  echo "AWS_SECRET_ACCESS_KEY:"
  echo "  [Retrieve from AWS IAM Console]"
  echo ""
fi

echo "📌 Update the following in your workflow:"
echo "   - Change AWS_REGION to '$AWS_REGION' in deploy-to-ec2.yml"
echo "   - Ensure ECR_REPOSITORY name matches: '$ECR_REPO_NAME'"
echo ""
