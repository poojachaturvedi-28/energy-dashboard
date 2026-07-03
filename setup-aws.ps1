# AWS Setup Script for Energy Dashboard Deployment (PowerShell)
# This script creates the necessary AWS resources for GitHub Actions deployment

param(
    [string]$AWSRegion = "us-east-1"
)

$ErrorActionPreference = "Stop"

$ECRRepoName = "energy-dashboard"
$IAMUserName = "github-actions-deploy"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "AWS Setup for Energy Dashboard" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Region: $AWSRegion" -ForegroundColor Yellow
Write-Host "ECR Repository: $ECRRepoName" -ForegroundColor Yellow
Write-Host "IAM User: $IAMUserName" -ForegroundColor Yellow
Write-Host ""

# Step 1: Create ECR Repository
Write-Host "Step 1/4: Creating ECR Repository..." -ForegroundColor Green
try {
    $ecrResponse = aws ecr create-repository `
        --repository-name $ECRRepoName `
        --region $AWSRegion `
        --query 'repository.repositoryUri' `
        --output text 2>$null
    $ECTURI = $ecrResponse
    Write-Host "✓ ECR repository created: $ECTURI" -ForegroundColor Green
}
catch {
    Write-Host "✓ ECR repository already exists" -ForegroundColor Yellow
    $ECTURI = aws ecr describe-repositories `
        --repository-names $ECRRepoName `
        --region $AWSRegion `
        --query 'repositories[0].repositoryUri' `
        --output text
}

# Step 2: Create IAM User
Write-Host ""
Write-Host "Step 2/4: Creating IAM User..." -ForegroundColor Green
try {
    aws iam create-user --user-name $IAMUserName 2>$null
    Write-Host "✓ IAM user created: $IAMUserName" -ForegroundColor Green
}
catch {
    Write-Host "✓ IAM user already exists: $IAMUserName" -ForegroundColor Yellow
}

# Step 3: Attach ECR Policy
Write-Host ""
Write-Host "Step 3/4: Attaching ECR permissions to IAM user..." -ForegroundColor Green
aws iam attach-user-policy `
    --user-name $IAMUserName `
    --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser 2>$null
Write-Host "✓ ECR policy attached" -ForegroundColor Green

# Step 4: Create and Display Access Keys
Write-Host ""
Write-Host "Step 4/4: Checking for existing access keys..." -ForegroundColor Green
$accessKeys = aws iam list-access-keys --user-name $IAMUserName --query 'AccessKeyMetadata[].AccessKeyId' --output text

if ([string]::IsNullOrWhiteSpace($accessKeys)) {
    Write-Host "Creating new access key..." -ForegroundColor Yellow
    $keyResponse = aws iam create-access-key --user-name $IAMUserName | ConvertFrom-Json
    $accessKeyId = $keyResponse.AccessKey.AccessKeyId
    $secretAccessKey = $keyResponse.AccessKey.SecretAccessKey
    Write-Host "✓ Access key created" -ForegroundColor Green
}
else {
    Write-Host "Access keys already exist for this user." -ForegroundColor Yellow
    Write-Host "⚠️  To use existing keys, retrieve them from AWS IAM console" -ForegroundColor Yellow
    Write-Host "   (The secret access key is not retrievable after initial creation)" -ForegroundColor Yellow
    $accessKeyId = $accessKeys
}

# Display Summary
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Setup Complete! ✓" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Save these values for GitHub Secrets:" -ForegroundColor Yellow
Write-Host ""
Write-Host "ECR_URI:"
Write-Host "  $ECTURI" -ForegroundColor Cyan
Write-Host ""
Write-Host "AWS_ACCESS_KEY_ID:"
Write-Host "  $accessKeyId" -ForegroundColor Cyan
Write-Host ""

if (-not [string]::IsNullOrWhiteSpace($secretAccessKey)) {
    Write-Host "AWS_SECRET_ACCESS_KEY:"
    Write-Host "  $secretAccessKey" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: Save the secret key securely! It won't be shown again." -ForegroundColor Red
    Write-Host ""
}
else {
    Write-Host "AWS_SECRET_ACCESS_KEY:"
    Write-Host "  [Retrieve from AWS IAM Console]" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "📌 Update the following in your workflow:" -ForegroundColor Yellow
Write-Host "   - Change AWS_REGION to '$AWSRegion' in deploy-to-ec2.yml" -ForegroundColor Yellow
Write-Host "   - Ensure ECR_REPOSITORY name matches: '$ECRRepoName'" -ForegroundColor Yellow
Write-Host ""

# Save to file
$outputFile = "aws-setup-results.txt"
@"
AWS Setup Results - $(Get-Date)
================================

ECR Repository URI: $ECTURI
AWS Access Key ID: $accessKeyId
IAM User: $IAMUserName
AWS Region: $AWSRegion

Remember: Save the secret access key securely!
"@ | Out-File -FilePath $outputFile
Write-Host "Results saved to: $outputFile" -ForegroundColor Green
