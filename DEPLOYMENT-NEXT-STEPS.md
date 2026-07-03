# 🚀 DEPLOYMENT SETUP - WHAT'S BEEN DONE & WHAT'S NEXT

## ✅ COMPLETED STEPS

All automated setup has been completed:

- [x] SSH key pair generated (`github-deploy-key` and `github-deploy-key.pub`)
- [x] GitHub Actions workflows created and pushed to GitHub
  - `deploy-to-ec2.yml` - Professional ECR-based deployment
  - `deploy-to-ec2-simple.yml` - Simple direct EC2 deployment
- [x] Comprehensive documentation created
- [x] AWS setup automation scripts created
- [x] All files committed and pushed to GitHub repository

---

## 📋 MANUAL STEPS YOU NEED TO COMPLETE

### Phase 1: AWS Account Setup (10 minutes)

**On your computer with AWS CLI installed:**

```bash
# Windows (PowerShell)
cd d:\energy\energy-dashboard
./setup-aws.ps1

# macOS/Linux
bash setup-aws.sh
```

This script will:
- ✓ Create ECR repository
- ✓ Create IAM user `github-actions-deploy`
- ✓ Generate access keys
- ✓ Output all values you need

**💾 Save the output! You'll need:**
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

---

### Phase 2: Launch EC2 Instance (10 minutes)

1. **Go to AWS Console:**
   - https://console.aws.amazon.com/ec2/

2. **Launch Instance:**
   - Click "Launch Instances"
   - Choose: **Ubuntu 22.04 LTS**
   - Instance type: **t3.micro** or **t3.small**
   - Create/select security group with:
     - SSH (22) from your IP
     - HTTP (80) from 0.0.0.0/0
     - HTTPS (443) from 0.0.0.0/0
   - Click "Launch"

3. **Install Docker on EC2:**
   ```bash
   # SSH into your instance
   ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
   
   # Install Docker
   sudo apt update && sudo apt install -y docker.io awscli
   sudo usermod -aG docker ubuntu
   
   # Logout and login again
   exit
   ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
   ```

4. **Add GitHub SSH key to EC2:**
   ```bash
   # On EC2
   mkdir -p ~/.ssh
   cat >> ~/.ssh/authorized_keys << 'EOF'
   ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC/lrhkXkwT9DFRBm0l2UcMY7/5roWQlVWn72VHjTbPdEUB3Xfs4GYp9Vf4nhfqFeSUubK0NRFnPfcy+5DnWqrdxGIOpbe7nK6enxUOZLox/2/4KsV2P3DqLGnqwksrrfnz7yokPTuJycQHEQ7kxvmtlOxRSLxnukrmUE9lJDCQUMcMGxE33NjURkUvUahpiliJO3tnvY8yPqyiNp/1ABMMh2GQ4mYAZGb9l58rw6wPepDa55GNMyCFNwsAB3QtGGx49Ge+eF8JcQLs6O0Qb6SDBjLzrhXtIFqHCygF7Vyuarmgd0zQCxnwiE5zpnaI1gwvj+srAOtLfV3fZeh7rqSAAXkelRNjmaRB9N2+ZC5ovsx2h5dNRVCkfGHLEichs0ah3deHRAk/NPfqPeeImu6muRj+CKvEbPj7eP97uu8nlKN9n68I3h+gtwTbbKyXrUzQiptIhZ/TmvhSA2OXlW8/bRoJ7Wlkn1luOKUFj7QYnATFdLPR5hvFF3zKP7un7sVNlXU+/Tc9Y1fKL17IyoK5osFCMRBLGJT4L94ONJ+P9MlutQyIvMcCNrwFgNfE/5D405cATrIKe9Qs1PidX5XA80ABtCtgQa7uT+qHL1rDKDN7mA6z4Q91bXhhltuYtpNXhG9TijY5zcLaZMkitRGYcYFT7RUDjgZ3Kn0Ij196QQ== github-actions
   EOF
   chmod 600 ~/.ssh/authorized_keys
   ```

5. **Get your EC2 Public IP:**
   - AWS Console → Instances → Your Instance
   - Copy the "Public IPv4 address" (e.g., `203.0.113.45`)

---

### Phase 3: Add GitHub Secrets (5 minutes)

1. **Go to GitHub:**
   - https://github.com/your-username/energy-dashboard
   - Settings → Secrets and variables → Actions

2. **Click "New repository secret" and add these 5 secrets:**

| Secret | Value | Source |
|--------|-------|--------|
| `AWS_ACCESS_KEY_ID` | (from AWS setup output) | From setup-aws script |
| `AWS_SECRET_ACCESS_KEY` | (from AWS setup output) | From setup-aws script |
| `EC2_HOST` | (your EC2 public IP) | EC2 Console |
| `EC2_USER` | `ubuntu` | ✓ Ready (copy as-is) |
| `EC2_PRIVATE_KEY` | (entire private key) | [GITHUB-SECRETS-CONFIG.md](GITHUB-SECRETS-CONFIG.md) |

**For EC2_PRIVATE_KEY:**
- Open [GITHUB-SECRETS-CONFIG.md](GITHUB-SECRETS-CONFIG.md)
- Copy the entire content from BEGIN to END markers
- Paste into GitHub secret

---

### Phase 4: Deploy! (30 seconds)

Once all secrets are added, your deployment is ready.

**Test deployment by making a commit:**

```bash
echo "# Deployment test" >> README.md
git add README.md
git commit -m "Test deployment"
git push origin main
```

**Watch it deploy:**
1. Go to GitHub repository
2. Click **Actions** tab
3. Click the workflow run
4. Watch the build and deployment

**After ~2-3 minutes, your app will be live at:**
```
http://YOUR_EC2_PUBLIC_IP/
```

---

## 🆘 QUICK TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| Workflow never starts | Check push was to `main` branch; might be set to `develop` in workflow |
| "Connection refused" | SSH key not added to EC2 authorized_keys; test with: `ssh -i github-deploy-key ubuntu@EC2_IP` |
| "ECR login failed" | Wrong AWS credentials; verify in GitHub secrets match AWS output |
| "Docker build fails" | Check Dockerfile syntax; run locally first: `docker build .` |
| "App returns 503" | SSH into EC2: `docker logs energy-app` to see error |

---

## 📁 FILES CREATED

- `.github/workflows/deploy-to-ec2.yml` - Main ECR deployment workflow
- `.github/workflows/deploy-to-ec2-simple.yml` - Simple deployment (no ECR)
- `.github/SECRETS-SETUP.md` - Detailed secrets documentation
- `DEPLOYMENT.md` - Comprehensive deployment guide
- `QUICK-START-DEPLOYMENT.md` - 5-step quick reference
- `GITHUB-SECRETS-CONFIG.md` - Secrets configuration (includes your public key)
- `setup-aws.ps1` - PowerShell AWS setup automation
- `setup-aws.sh` - Bash AWS setup automation

---

## 📚 DOCUMENTATION

Read these in order:

1. **[QUICK-START-DEPLOYMENT.md](QUICK-START-DEPLOYMENT.md)** - Start here (2 min read)
2. **[GITHUB-SECRETS-CONFIG.md](GITHUB-SECRETS-CONFIG.md)** - Secret values to copy
3. **[DEPLOYMENT.md](DEPLOYMENT.md)** - Full reference guide
4. **[.github/SECRETS-SETUP.md](.github/SECRETS-SETUP.md)** - Detailed secrets info

---

## ✨ YOUR KEYS (Keep Safe!)

### Public Key Location
```
~/.ssh/github-deploy-key.pub
```

Already added to EC2 in Phase 2 step 4.

### Private Key Location
```
~/.ssh/github-deploy-key
```

Never commit this to git. Already in GitHub Secrets (EC2_PRIVATE_KEY).

---

## 🎯 SUCCESS CRITERIA

You'll know it's working when:

✅ GitHub Actions "Deploy to AWS EC2" workflow completes  
✅ EC2 instance has running `energy-app` container  
✅ App responds at `http://YOUR_EC2_IP/`  
✅ Can see dashboard charts and KPIs  

---

## ⏱️ ESTIMATED TIME

- Phase 1 (AWS): ~10 min
- Phase 2 (EC2): ~10 min  
- Phase 3 (Secrets): ~5 min
- Phase 4 (Deploy): ~2-3 min build
- **Total: ~30 minutes**

---

## 🔐 SECURITY NOTES

✓ Private key is in GitHub Secrets (encrypted)  
✓ AWS credentials rotated automatically (or on demand)  
✓ EC2 security group restricts access  
✓ SSH key-based auth (no passwords)  

🎉 **You're all set! Follow the phases above and your Energy Dashboard will be live on AWS EC2!**

