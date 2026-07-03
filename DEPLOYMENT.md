# AWS EC2 Deployment Guide

This guide walks you through setting up GitHub Actions to automatically deploy the Energy Dashboard to AWS EC2.

## Prerequisites

- AWS Account with EC2 and ECR access
- GitHub repository with this project
- AWS IAM user with programmatic access
- EC2 instance running (Ubuntu recommended)
- Docker installed on your EC2 instance

---

## Step 1: Prepare Your EC2 Instance

### 1.1 Launch an EC2 Instance

1. Go to [AWS EC2 Console](https://console.aws.amazon.com/ec2/)
2. Click **Launch Instances**
3. Choose **Ubuntu 22.04 LTS** (or latest)
4. Select instance type (t3.micro or t3.small recommended)
5. Configure security group:
   - Allow SSH (port 22) from your IP
   - Allow HTTP (port 80) from 0.0.0.0/0
   - Allow HTTPS (port 443) from 0.0.0.0/0

### 1.2 Install Docker on EC2

```bash
# Connect to your instance
ssh -i your-key.pem ubuntu@your-ec2-public-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install -y docker.io

# Add ubuntu user to docker group
sudo usermod -aG docker ubuntu

# Verify installation
docker --version
```

### 1.3 Install AWS CLI on EC2

```bash
sudo apt install -y awscli
```

---

## Step 2: Create AWS Resources

### 2.1 Create ECR Repository

```bash
aws ecr create-repository \
  --repository-name energy-dashboard \
  --region us-east-1
```

**Output:** Copy the repository URI (looks like `123456789.dkr.ecr.us-east-1.amazonaws.com/energy-dashboard`)

### 2.2 Create IAM User for GitHub Actions

1. Go to [IAM Console](https://console.aws.amazon.com/iam/)
2. Click **Users** → **Create user**
3. Name: `github-actions-deploy`
4. Attach policies:
   - `AmazonEC2ContainerRegistryPowerUser` (for ECR)
   - Custom inline policy for EC2 (see below):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2-instance-connect:SendSSHPublicKey",
        "ec2:DescribeInstances"
      ],
      "Resource": "*"
    }
  ]
}
```

5. Go to **Security credentials** tab
6. Click **Create access key** → **Application running outside AWS**
7. **Save** the Access Key ID and Secret Access Key

---

## Step 3: Generate SSH Key Pair for Deployment

### 3.1 Generate Key Locally

```bash
# On your local machine
ssh-keygen -t rsa -b 4096 -f github-deploy-key -C "github-actions"

# This creates:
# - github-deploy-key (private key)
# - github-deploy-key.pub (public key)
```

### 3.2 Add Public Key to EC2

```bash
# Add to EC2 authorized_keys
cat github-deploy-key.pub | ssh -i your-main-key.pem ubuntu@your-ec2-public-ip \
  "cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

# Test the connection
ssh -i github-deploy-key ubuntu@your-ec2-public-ip "echo Connected successfully!"
```

---

## Step 4: Configure GitHub Secrets

In your GitHub repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add the following secrets:

| Secret Name | Value |
|---|---|
| `AWS_ACCESS_KEY_ID` | From IAM user (Step 2.2) |
| `AWS_SECRET_ACCESS_KEY` | From IAM user (Step 2.2) |
| `EC2_HOST` | Your EC2 public IP or domain name |
| `EC2_USER` | `ubuntu` (or your SSH user) |
| `EC2_PRIVATE_KEY` | Contents of `github-deploy-key` file (private key) |

### How to Add Secrets:

```bash
# 1. View the private key
cat github-deploy-key

# 2. Copy the entire output
# 3. In GitHub, click "New repository secret"
# 4. Name: EC2_PRIVATE_KEY
# 5. Paste the entire private key content
```

---

## Step 5: Configure Workflow Parameters

Edit [.github/workflows/deploy-to-ec2.yml](.github/workflows/deploy-to-ec2.yml):

```yaml
env:
  AWS_REGION: us-east-1          # ← Change to your AWS region
  ECR_REPOSITORY: energy-dashboard
  CONTAINER_NAME: energy-app
```

---

## Step 6: Deploy

### Automatic Deployment (on push to main)

```bash
git add .
git commit -m "Deploy to EC2"
git push origin main
```

The workflow will automatically:
1. ✓ Build Docker image
2. ✓ Push to ECR
3. ✓ Deploy to EC2
4. ✓ Verify the application is running

### Manual Deployment (anytime)

1. Go to GitHub repository
2. Click **Actions** tab
3. Select **Deploy to AWS EC2** workflow
4. Click **Run workflow** → **Run workflow**

---

## Step 7: Access Your Application

Once deployed, visit:

```
http://your-ec2-public-ip/
```

---

## Troubleshooting

### Workflow Fails at "Build" Step

**Problem:** Docker build fails
**Solution:**
- Check `Dockerfile` is correct
- Verify `requirements.txt` has all dependencies
- Check Docker image size isn't exceeding limits

### Workflow Fails at "Deploy" Step

**Problem:** SSH connection fails
**Solution:**
- Verify EC2 security group allows port 22 from GitHub Actions IP
- Check private key is correctly added to secrets (with newlines preserved)
- Test SSH connection manually: `ssh -i github-deploy-key ubuntu@your-ec2-public-ip`

### Application Not Responding

**Problem:** Deployment completes but app returns 503 error
**Solution:**
- SSH into EC2 and check container logs:
  ```bash
  docker logs energy-app
  ```
- Verify port mapping: `docker ps`
- Check EC2 security group allows port 80 from 0.0.0.0/0

### ECR Login Fails

**Problem:** "Unable to login to ECR"
**Solution:**
- Verify IAM user has `AmazonEC2ContainerRegistryPowerUser` policy
- Verify AWS credentials are correct in GitHub secrets
- Verify AWS region matches ECR repository region

---

## Advanced: Using Domain Name

To use a custom domain instead of IP address:

1. Point your domain DNS to your EC2 public IP
2. Install Nginx as reverse proxy on EC2:

```bash
sudo apt install -y nginx

# Create Nginx config
sudo nano /etc/nginx/sites-available/default
```

Add this configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Then:

```bash
sudo systemctl restart nginx
```

Now your app is accessible at `http://your-domain.com`

---

## Advanced: SSL with Let's Encrypt

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
```

---

## Monitoring & Maintenance

### View Deployment Logs

```bash
# GitHub Actions logs visible in Actions tab

# EC2 application logs
ssh -i github-deploy-key ubuntu@your-ec2-public-ip
docker logs -f energy-app
```

### Update and Redeploy

```bash
# Make changes to your code
git add .
git commit -m "Update dashboard"
git push origin main

# Workflow runs automatically
```

### Manual Container Management on EC2

```bash
# View running containers
docker ps

# View container logs
docker logs energy-app

# Stop container
docker stop energy-app

# Restart container
docker start energy-app

# Remove old images
docker image prune -f
```

---

## Cost Optimization

- Use **t3.micro** or **t3.small** EC2 instances (eligible for free tier)
- Set up **auto-shutdown** for non-production instances
- Monitor ECR storage and clean up old images
- Use **CloudWatch** to monitor costs

---

## Security Best Practices

✓ Keep EC2 security group restricted (only allow necessary ports)
✓ Use SSH keys instead of passwords
✓ Rotate access keys regularly
✓ Use IAM roles for service-to-service communication
✓ Enable EC2 instance monitoring
✓ Keep Docker images updated
✓ Use private ECR repositories

---

## Next Steps

- [ ] Test deployment workflow
- [ ] Set up monitoring/alerts with CloudWatch
- [ ] Configure custom domain and SSL
- [ ] Set up automated backups for data
- [ ] Create CI tests before deployment

