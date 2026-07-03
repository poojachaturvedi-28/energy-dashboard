# ✅ UPDATE: New EC2 Configuration

Your EC2 instance is now live! Update these values:

---

## 🔧 Update GitHub Secret: EC2_HOST

**New value:** `3.89.139.18`

**Steps:**
1. Go to GitHub → Your repository
2. Settings → Secrets and variables → Actions
3. Find `EC2_HOST` secret
4. Click the pencil icon to edit
5. Change value to: `3.89.139.18`
6. Click "Update secret"

---

## 📍 Access Your Application

After updating the secret and pushing a new commit:

```
http://3.89.139.18:8000/
```

**OR visit directly:**
- Dashboard: http://3.89.139.18:8000
- API endpoints: http://3.89.139.18:8000/api/...

---

## ✅ What Was Updated

✓ Port changed from 80 → 8000
✓ Workflows updated in `.github/workflows/`
✓ Both deployment workflows now use port 8000

---

## 🚀 Deploy & Test

### Option 1: Automatic (Recommended)
```bash
# Make a change and push
echo "# Deployed" >> README.md
git add README.md
git commit -m "Test deployment with port 8000"
git push origin main
```

Watch the deployment in: GitHub → Actions tab

### Option 2: Manual Trigger
1. GitHub → Actions tab
2. Select "Deploy to AWS EC2" workflow
3. Click "Run workflow"
4. Select branch: `main`
5. Click green "Run workflow" button

---

## 🔍 Verify Deployment

### Check if app is running:
```bash
curl http://3.89.139.18:8000/
```

### SSH into EC2 to check logs:
```bash
ssh -i ~/.ssh/github-deploy-key ubuntu@3.89.139.18
docker logs -f energy-app
```

### Check container status:
```bash
docker ps
```

---

## 📋 Checklist

- [ ] Updated `EC2_HOST` secret on GitHub to `3.89.139.18`
- [ ] Workflow files updated with port 8000 (already done ✓)
- [ ] Pushed changes to GitHub
- [ ] Deployment workflow completed successfully
- [ ] App accessible at http://3.89.139.18:8000/

---

## ⚠️ Troubleshooting

### "Connection refused" on port 8000
```bash
# SSH into EC2
ssh -i ~/.ssh/github-deploy-key ubuntu@3.89.139.18

# Check if container is running
docker ps

# Check logs
docker logs energy-app

# Restart if needed
docker restart energy-app
```

### "Permission denied (publickey)"
- Verify EC2_PRIVATE_KEY secret is correct
- Test SSH directly: `ssh -i ~/.ssh/github-deploy-key ubuntu@3.89.139.18`

### Workflow still shows old IP
- Clear browser cache
- Hard refresh (Ctrl+Shift+R)
- Verify GitHub secret was saved correctly

---

## 📚 Related Documentation

- [DEPLOYMENT-NEXT-STEPS.md](DEPLOYMENT-NEXT-STEPS.md)
- [QUICK-START-DEPLOYMENT.md](QUICK-START-DEPLOYMENT.md)
- [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 🎉 You're Live!

Your Energy Dashboard is now deployed to:
### **http://3.89.139.18:8000/**

