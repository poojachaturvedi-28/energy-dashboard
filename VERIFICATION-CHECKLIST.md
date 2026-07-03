# ✅ PRE-DEPLOYMENT VERIFICATION CHECKLIST

Run through this checklist to ensure everything is configured correctly before deployment.

---

## 1️⃣ GITHUB SECRETS VERIFICATION

**CRITICAL:** All 5 secrets must be set correctly.

### Location
GitHub → Your Repository → Settings → Secrets and variables → Actions

### Required Secrets

#### ✅ AWS_ACCESS_KEY_ID
- [ ] Secret exists
- [ ] Value starts with `AKIA` (20 characters)
- [ ] Example: `AKIA1234567890ABCDEF`

#### ✅ AWS_SECRET_ACCESS_KEY  
- [ ] Secret exists
- [ ] Value is 40+ characters with special characters
- [ ] Not beginning with `AWS`

#### ✅ EC2_HOST ⚠️ CRITICAL
- [ ] Secret exists
- [ ] Value is: `3.89.139.18` (exact IP)
- [ ] NOT a domain or old IP
- [ ] Recheck: This is the public IP of your EC2 instance

#### ✅ EC2_USER
- [ ] Secret exists
- [ ] Value is: `ubuntu` (exact)

#### ✅ EC2_PRIVATE_KEY
- [ ] Secret exists
- [ ] Starts with: `-----BEGIN OPENSSH PRIVATE KEY-----`
- [ ] Ends with: `-----END OPENSSH PRIVATE KEY-----`
- [ ] Contains newlines (GitHub preserves them)
- [ ] Should be 1700+ characters long

**Test:** 
```bash
ssh -i ~/.ssh/github-deploy-key ubuntu@3.89.139.18 "echo 'Connection OK'"
```

---

## 2️⃣ EC2 INSTANCE VERIFICATION

SSH into your EC2 instance and verify:

```bash
# Connect
ssh -i ~/.ssh/github-deploy-key ubuntu@3.89.139.18

# Run these checks on EC2:
```

### Docker Installation
```bash
docker --version
# Should show: Docker version 20.x or higher
```

### AWS CLI Configuration
```bash
aws --version
aws sts get-caller-identity
# Should show your AWS account info
```

### SSH Key Setup
```bash
cat ~/.ssh/authorized_keys | grep github-actions
# Should output your github-deploy-key.pub content
```

### Port 8000 Availability
```bash
# Check if something is already using port 8000
sudo lsof -i :8000
# Should return nothing (port is free)
```

### Security Group Settings
On AWS Console → EC2 → Security Groups:
- [ ] Inbound TCP 22 (SSH) from your IP
- [ ] Inbound TCP 8000 (App) from 0.0.0.0/0
- [ ] Inbound TCP 443 (HTTPS) from 0.0.0.0/0 (optional)
- [ ] Outbound: all traffic allowed (default)

---

## 3️⃣ WORKFLOW FILE VERIFICATION

Check the workflow files are correctly configured:

### Location
`.github/workflows/deploy-to-ec2.yml`

### Critical Lines
```yaml
env:
  AWS_REGION: us-east-1          # ✓ Correct region
  ECR_REPOSITORY: energy-dashboard
  CONTAINER_NAME: energy-app

# Port mapping should be: -p 8000:5000
# Check these lines exist:
# -p 8000:5000  (NOT -p 80:5000)
```

---

## 4️⃣ DOCKERFILE VERIFICATION

Check `Dockerfile` configuration:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"]
```

- [ ] Base image is python:3.12-slim ✓
- [ ] EXPOSE 5000 (container port) ✓
- [ ] CMD uses gunicorn ✓

---

## 5️⃣ APPLICATION REQUIREMENTS

Check `requirements.txt`:

```
flask==3.0.3
gunicorn==22.0.0
pandas==2.2.2
openpyxl==3.1.2
```

- [ ] flask installed ✓
- [ ] gunicorn installed ✓
- [ ] pandas installed ✓

---

## 6️⃣ GIT CONFIGURATION

Verify your local git repo is clean:

```bash
cd d:\energy\energy-dashboard

# Check status
git status
# Should show: "nothing to commit, working tree clean"

# Check branch
git branch
# Should show: * main

# Check remote
git remote -v
# Should show GitHub URLs
```

- [ ] All changes committed
- [ ] On main branch
- [ ] Remote points to GitHub

---

## 7️⃣ DEPLOYMENT WORKFLOW STATUS

After pushing changes, verify workflow triggered:

1. Go to: https://github.com/poojachaturvedi-28/energy-dashboard/actions
2. You should see a new workflow run
3. Status will be "In progress" (orange dot)

---

## 8️⃣ NETWORK CONNECTIVITY TEST

From your computer, test connectivity to EC2:

```bash
# Test SSH
ssh -i ~/.ssh/github-deploy-key ubuntu@3.89.139.18 "echo OK"

# Test HTTP (after deployment starts)
curl http://3.89.139.18:8000/ -I
```

- [ ] SSH works
- [ ] Port 8000 is accessible

---

## ⏱️ DEPLOYMENT TIMELINE

After pushing code, expect:

| Stage | Time | Status |
|-------|------|--------|
| GitHub Actions Triggered | Immediate | ⏳ Pending |
| Build Docker Image | 2-3 min | 🔨 Building |
| Push to ECR | 1-2 min | 📤 Pushing |
| SSH to EC2 | 30 sec | 🔌 Connecting |
| Pull Image & Run | 2-3 min | 🚀 Deploying |
| Verification | 1 min | ✅ Testing |
| **TOTAL** | **5-10 min** | **Complete** |

---

## 🆘 WHAT TO DO IF STUCK

### Workflow Stuck at "In progress" > 15 minutes
- Cancel workflow and retry: Actions → workflow → Cancel
- Push a new commit to trigger again

### SSH Connection Fails
```bash
# Test SSH key
ssh -i ~/.ssh/github-deploy-key -v ubuntu@3.89.139.18

# Common issues:
# 1. Wrong IP in EC2_HOST secret
# 2. Private key file corrupted
# 3. Public key not in EC2 authorized_keys
```

### Docker Build Fails
- Check Dockerfile syntax locally: `docker build .`
- Check requirements.txt has all dependencies
- Check network/firewall blocking pip downloads

### App Won't Start
```bash
ssh -i ~/.ssh/github-deploy-key ubuntu@3.89.139.18
docker logs energy-app
# Look for error messages
```

### Port 8000 Not Responding
- Check EC2 security group allows inbound 8000
- Check container is running: `docker ps`
- Check port inside container: `docker exec energy-app netstat -tlnp`

---

## ✅ FINAL CHECKLIST

Before considering deployment "complete":

- [ ] GitHub Actions workflow shows ✅ (green)
- [ ] No errors in workflow logs
- [ ] SSH to EC2 works
- [ ] `docker ps` shows running `energy-app` container
- [ ] `curl http://3.89.139.18:8000/` returns 200 OK
- [ ] Dashboard loads in browser
- [ ] Charts display with data
- [ ] API endpoints respond: `curl http://3.89.139.18:8000/api/metrics`

---

## 📞 QUICK COMMANDS

Copy-paste these for quick testing:

```bash
# Test SSH
ssh -i ~/.ssh/github-deploy-key ubuntu@3.89.139.18

# Check container
docker ps -a | grep energy-app

# View logs
docker logs -f energy-app

# Test app locally on EC2
curl http://localhost:5000/

# Test app from computer
curl http://3.89.139.18:8000/

# Check port listening
ss -tlnp | grep 8000

# Restart container
docker restart energy-app

# Remove old container
docker stop energy-app && docker rm energy-app
```

---

## 📚 REFERENCE FILES

- [DEPLOYMENT-STATUS.md](DEPLOYMENT-STATUS.md) - Real-time monitoring
- [UPDATE-IP-PORT.md](UPDATE-IP-PORT.md) - IP and port configuration
- [DEPLOYMENT.md](DEPLOYMENT.md) - Full deployment guide
- [QUICK-START-DEPLOYMENT.md](QUICK-START-DEPLOYMENT.md) - Quick reference

---

**Run this checklist before and after deployment to ensure everything is working! ✅**

