# Quick Start: Deploy to AWS EC2 in 5 Steps

## Choice: Which Workflow?

| Workflow | Pros | Cons | Best For |
|---|---|---|---|
| **deploy-to-ec2.yml** (ECR) | Fast, professional, scalable | More setup, AWS costs | Production deployments |
| **deploy-to-ec2-simple.yml** | Simple, fewer AWS resources | Slower builds | Development, learning |

---

## Quick Start (ECR - Professional)

### Step 1: Launch EC2 & Install Docker (5 min)

```bash
# SSH into EC2
ssh -i your-key.pem ubuntu@YOUR_EC2_IP

# Install Docker
sudo apt update && sudo apt install -y docker.io awscli
sudo usermod -aG docker ubuntu
```

### Step 2: Create AWS Resources (5 min)

```bash
# Create ECR repo
aws ecr create-repository --repository-name energy-dashboard --region us-east-1

# Create IAM user 'github-actions-deploy'
# Attach: AmazonEC2ContainerRegistryPowerUser policy
# Generate Access Key
```

### Step 3: Create SSH Keys (3 min)

```bash
# On your computer
ssh-keygen -t rsa -b 4096 -f github-deploy-key -C "github-actions"

# Add public key to EC2
ssh -i your-key.pem ubuntu@YOUR_EC2_IP 'cat >> ~/.ssh/authorized_keys' < github-deploy-key.pub
```

### Step 4: Add Secrets to GitHub (2 min)

**Go to:** Repository → Settings → Secrets and variables → Actions

Add these 5 secrets:

```
AWS_ACCESS_KEY_ID          = [from IAM user]
AWS_SECRET_ACCESS_KEY      = [from IAM user]
EC2_HOST                   = [your EC2 public IP]
EC2_USER                   = ubuntu
EC2_PRIVATE_KEY            = [contents of github-deploy-key file]
```

### Step 5: Deploy (30 sec)

```bash
git push origin main
```

✓ Done! Watch deployment in GitHub Actions tab

---

## Quick Start (Simple - No ECR)

### Step 1: Launch EC2 & Install Docker (5 min)

```bash
ssh -i your-key.pem ubuntu@YOUR_EC2_IP
sudo apt update && sudo apt install -y docker.io
sudo usermod -aG docker ubuntu
```

### Step 2: Create SSH Keys (3 min)

```bash
ssh-keygen -t rsa -b 4096 -f github-deploy-key -C "github-actions"
ssh -i your-key.pem ubuntu@YOUR_EC2_IP 'cat >> ~/.ssh/authorized_keys' < github-deploy-key.pub
```

### Step 3: Add Secrets to GitHub (2 min)

Add 3 secrets:

```
EC2_HOST = [your EC2 public IP]
EC2_USER = ubuntu
EC2_PRIVATE_KEY = [contents of github-deploy-key file]
```

### Step 4: Deploy (30 sec)

```bash
git push origin main
```

---

## Access Your App

After deployment succeeds:

```
http://YOUR_EC2_IP/
```

---

## Troubleshooting

| Problem | Solution |
|---|---|
| SSH connection fails | Check security group allows port 22; verify private key is correct |
| Docker build fails | Check Dockerfile, run `docker build .` locally to debug |
| App not responding | SSH into EC2: `docker logs energy-app` |
| ECR login fails | Verify IAM permissions; check AWS credentials in secrets |

---

## View Logs

**GitHub Actions Logs:**
- Repository → Actions tab → click workflow run

**EC2 Application Logs:**
```bash
ssh -i github-deploy-key ubuntu@YOUR_EC2_IP
docker logs -f energy-app
```

---

## Update & Redeploy

```bash
# Make changes
git add .
git commit -m "Update"
git push origin main

# Workflow runs automatically
```

---

## Security Checklist

- [ ] EC2 security group: SSH (22) restricted to your IP
- [ ] EC2 security group: HTTP (80) from 0.0.0.0/0
- [ ] SSH keys stored safely, not committed to git
- [ ] AWS access keys rotated regularly
- [ ] Using strong EC2 passwords or key pairs

---

## Common AWS Costs

- **t3.micro EC2**: $0 - $8/month (eligible for free tier)
- **ECR storage**: ~$0.10/GB/month
- **Data transfer**: ~$0.02/GB
- **Total**: Usually under $10/month for hobby projects

---

## Next Steps

1. **Test deployment** with a simple change
2. **Enable monitoring** - CloudWatch alarms for high CPU/memory
3. **Add domain** - Point your domain to EC2 IP
4. **Enable SSL** - Use Let's Encrypt with Certbot
5. **Set up backups** - Periodic data snapshots

---

## Full Guide

For more details, see [DEPLOYMENT.md](DEPLOYMENT.md)

