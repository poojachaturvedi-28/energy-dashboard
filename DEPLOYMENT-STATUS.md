# 🚀 DEPLOYMENT RETRY - FULL STATUS CHECK

## ✅ COMPLETED STEPS

✓ Deployment commit pushed to GitHub  
✓ GitHub Actions workflow **triggered**  
✓ Port mapping updated: `8000:5000`  
✓ EC2 IP: `3.89.139.18`  

---

## 📊 DEPLOYMENT STATUS

**Workflow Status:** Check at: https://github.com/poojachaturvedi-28/energy-dashboard/actions

Expected timeline:
- **Build & Push to ECR**: 2-3 minutes
- **Deploy to EC2**: 2-3 minutes  
- **Verification**: 1-2 minutes
- **Total**: 5-8 minutes

---

## 🔍 REAL-TIME MONITORING

### 1. Monitor GitHub Actions (Recommended)
```
https://github.com/poojachaturvedi-28/energy-dashboard/actions
```

Click the latest workflow run to see live logs.

### 2. SSH into EC2 to Check Status
```bash
# Connect to EC2
ssh -i ~/.ssh/github-deploy-key ubuntu@3.89.139.18

# Check container status
docker ps -a

# View deployment logs
docker logs -f energy-app

# Check port 8000 is listening
netstat -tlnp | grep 8000
# OR
ss -tlnp | grep 8000

# Test application locally on EC2
curl http://localhost:5000/
```

### 3. Test from Your Computer
```bash
# Simple connectivity test
curl http://3.89.139.18:8000/

# With verbose output
curl -v http://3.89.139.18:8000/

# Check if port responds
telnet 3.89.139.18 8000
```

---

## ✅ SUCCESS CHECKLIST

After ~5-8 minutes, verify:

- [ ] GitHub Actions workflow shows ✅ (green check)
- [ ] EC2 container `energy-app` is running
  ```bash
  docker ps | grep energy-app
  ```
- [ ] Port 8000 is listening
  ```bash
  curl http://3.89.139.18:8000/
  ```
- [ ] Dashboard loads with charts at http://3.89.139.18:8000/

---

## 📋 PRE-DEPLOYMENT VERIFICATION

### Secrets Configured ✓
- [x] `AWS_ACCESS_KEY_ID` - Set
- [x] `AWS_SECRET_ACCESS_KEY` - Set
- [x] `EC2_HOST` - Updated to `3.89.139.18` (REQUIRED)
- [x] `EC2_USER` - `ubuntu`
- [x] `EC2_PRIVATE_KEY` - Set

### Workflow Files ✓
- [x] `.github/workflows/deploy-to-ec2.yml` - Port 8000 configured
- [x] `.github/workflows/deploy-to-ec2-simple.yml` - Port 8000 configured
- [x] `Dockerfile` - Ready
- [x] `requirements.txt` - Dependencies defined

### EC2 Instance ✓
- [x] IP: `3.89.139.18`
- [x] Port 8000 open in security group
- [x] Docker installed
- [x] AWS CLI configured (for ECR login)

---

## 🆘 TROUBLESHOOTING

### Workflow Fails - Check GitHub Actions Logs
1. Go to Actions tab
2. Click the failed workflow
3. Click the failed job (Build or Deploy)
4. Read error message
5. Common issues:
   - **"Secrets not found"** → Verify all 5 secrets are set
   - **"SSH connection failed"** → Check EC2_HOST secret updated
   - **"Docker build failed"** → Check requirements.txt and Dockerfile

### EC2 Shows "Connection refused"
```bash
# Check if Docker daemon is running
sudo service docker status

# Check if container exists
docker ps -a

# Check container logs for errors
docker logs energy-app

# Restart container if needed
docker restart energy-app
```

### Port 8000 Not Responding
```bash
# Check if port is in use
sudo lsof -i :8000
# or
ss -tlnp | grep 8000

# Check firewall (EC2 security group)
# AWS Console → EC2 → Security Groups → Inbound rules
# Should have: TCP 8000 from 0.0.0.0/0

# Test locally on EC2
curl http://localhost:5000
```

### App Loads But No Data
- Wait for container to fully start (may take 30 seconds)
- Check if data files exist: `/app/data/energy.csv`
- Check container logs: `docker logs energy-app`

---

## 📝 MANUAL DEPLOYMENT (If Automated Fails)

If the workflow continues to fail, deploy manually on EC2:

```bash
# SSH into EC2
ssh -i ~/.ssh/github-deploy-key ubuntu@3.89.139.18

# Clone the repository
git clone https://github.com/poojachaturvedi-28/energy-dashboard.git
cd energy-dashboard

# Login to ECR (replace with your credentials)
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ECR_URI

# Build Docker image
docker build -t energy-dashboard:latest .

# Stop old container
docker stop energy-app || true
docker rm energy-app || true

# Run new container
docker run -d \
  --name energy-app \
  --restart unless-stopped \
  -p 8000:5000 \
  energy-dashboard:latest

# Check logs
docker logs -f energy-app
```

---

## 📊 NEXT STEPS

1. **Monitor deployment** (5-8 minutes)
   - Go to: https://github.com/poojachaturvedi-28/energy-dashboard/actions
   
2. **After workflow completes successfully:**
   - Visit: http://3.89.139.18:8000/
   - Should see the Energy Dashboard with charts

3. **If any errors:**
   - Check logs in GitHub Actions
   - SSH into EC2: `ssh -i ~/.ssh/github-deploy-key ubuntu@3.89.139.18`
   - Run: `docker logs energy-app`

4. **Test the application:**
   ```bash
   curl http://3.89.139.18:8000/api/metrics
   ```

---

## 💾 Key Information

| Item | Value |
|------|-------|
| **EC2 IP** | `3.89.139.18` |
| **Port** | `8000` |
| **Dashboard URL** | `http://3.89.139.18:8000/` |
| **SSH** | `ssh -i ~/.ssh/github-deploy-key ubuntu@3.89.139.18` |
| **Container Name** | `energy-app` |
| **Docker Image** | `energy-dashboard:latest` |

---

## 🎯 DEPLOYMENT COMPLETE WHEN:

✅ GitHub Actions shows green checkmark  
✅ `curl http://3.89.139.18:8000/` returns HTML  
✅ Dashboard loads and displays charts  
✅ `docker ps` shows running `energy-app` container  

---

**⏱️ Check back in 5-10 minutes for deployment completion!**

