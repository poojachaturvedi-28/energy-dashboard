# GitHub Secrets Configuration - Copy These Values

This file contains the values you need to add to your GitHub repository secrets.

**Location:** Go to: Repository → Settings → Secrets and variables → Actions → New repository secret

---

## ✅ STEP 1: SSH KEYS (Already Generated)

### Secret: EC2_PRIVATE_KEY
**Status:** ✅ Ready to copy

Copy the ENTIRE content below (including BEGIN/END markers):

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAACFwAAAAdzc2gtcn
NhAAAAAwEAAQAAAgEAv5a4ZF5ME/QxUQZtJdlHDGO/+a6FkJVVp+9lR402z3RFAd137OBm
KfVX+J4X6hXklLmytDURZz33MvuQ51qq3cRiDqW3u5yunp8VDmS6Mf9v+CrFdj9w6ixp6s
JLK6358+8qJD07icnEBxEO5Mb5rZTsUUi8Z7pK5lBPZSQwkFDHDBsRN9zY1EZFL1GoaYpY
iTt7Z72PMj6sojaf9QATDIdhkOJmAGRm/ZefK8OsD3qQ2ueRjTMghTcLAAd0LRhsePRnvn
hfCXEC7OjtEG+kgwYy864V7SBahwsoBe1crmq5oHdM0AsZ8IhOc6Z2iNYML4/rKwDrS31d
32Xoe66kgAF5HpUTY5mkQfTdvmQuaL7MdoeXTUVQpHxhyxInIbNGod3Xh0QJPzT36j3niJ
ruprkY/girxGz4+3j/e7rvJ5SjfZ+vCN4foLcE22ysl61M0IqbSIWf05r4UgNjl5VvP20a
Ce1pZJ9ZbjilBY+0GJwExXSz0eYbxRd8yj+7p+7FTZV1Pv03PWNXyi9eyMqCuaLBQjEQSx
iU+C/eDjSfj/TJbrUMiLzHAja8BYDXxP+Q+NOXAE6yCnvULNT4nV+VwPNAAbQrYEGu7k/q
hy9awygze5gOs+EPdW14YZbbmLaTV4RvU4o2Oc3C2mTJIrURmHGBU+0VA44Gdyp9CI9fek
EAAA
-----END OPENSSH PRIVATE KEY-----
```

### Secret: EC2_USER
**Status:** ✅ Ready

Value (copy exactly):
```
ubuntu
```

### Secret: EC2_PUBLIC_KEY
**Status:** ℹ️ For reference only (not needed in secrets, but keep safe)

This is used to connect EC2 authorized_keys:
```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC/lrhkXkwT9DFRBm0l2UcMY7/5roWQlVWn72VHjTbPdEUB3Xfs4GYp9Vf4nhfqFeSUubK0NRFnPfcy+5DnWqrdxGIOpbe7nK6enxUOZLox/2/4KsV2P3DqLGnqwksrrfnz7yokPTuJycQHEQ7kxvmtlOxRSLxnukrmUE9lJDCQUMcMGxE33NjURkUvUahpiliJO3tnvY8yPqyiNp/1ABMMh2GQ4mYAZGb9l58rw6wPepDa55GNMyCFNwsAB3QtGGx49Ge+eF8JcQLs6O0Qb6SDBjLzrhXtIFqHCygF7Vyuarmgd0zQCxnwiE5zpnaI1gwvj+srAOtLfV3fZeh7rqSAAXkelRNjmaRB9N2+ZC5ovsx2h5dNRVCkfGHLEichs0ah3deHRAk/NPfqPeeImu6muRj+CKvEbPj7eP97uu8nlKN9n68I3h+gtwTbbKyXrUzQiptIhZ/TmvhSA2OXlW8/bRoJ7Wlkn1luOKUFj7QYnATFdLPR5hvFF3zKP7un7sVNlXU+/Tc9Y1fKL17IyoK5osFCMRBLGJT4L94ONJ+P9MlutQyIvMcCNrwFgNfE/5D405cATrIKe9Qs1PidX5XA80ABtCtgQa7uT+qHL1rDKDN7mA6z4Q91bXhhltuYtpNXhG9TijY5zcLaZMkitRGYcYFT7RUDjgZ3Kn0Ij196QQ== github-actions
```

---

## 🔴 STEP 2: AWS SECRETS (You Need to Create These)

**IMPORTANT:** These require your AWS account setup. Run the AWS setup script first.

### Option A: Using AWS CLI (Recommended)

On your computer with AWS CLI installed:

```bash
# Windows (PowerShell)
cd d:\energy\energy-dashboard
./setup-aws.ps1

# macOS/Linux
bash setup-aws.sh
```

The script will output all the values you need.

### Option B: Manual Setup via AWS Console

#### Secret: AWS_ACCESS_KEY_ID
1. Go to https://console.aws.amazon.com/iam/
2. Click Users → github-actions-deploy (create if doesn't exist)
3. Security credentials → Create access key
4. Copy the "Access key ID"

#### Secret: AWS_SECRET_ACCESS_KEY
1. From the same access key creation (Step B, Step 3)
2. Copy the "Secret access key"
3. ⚠️ Save it immediately - it's only shown once!

---

## 📋 STEP 3: EC2 SECRETS (After Launching EC2)

### Secret: EC2_HOST
1. Launch EC2 instance on AWS Console
2. Go to Instances → Your Instance
3. Copy "Public IPv4 address" (e.g., `203.0.113.45`)
   OR copy "Public IPv4 DNS" (e.g., `ec2-203-0-113-45.compute-1.amazonaws.com`)

---

## 🚀 STEP 4: Add All Secrets to GitHub

Go to: **Repository Settings → Secrets and variables → Actions**

Click "New repository secret" for each:

| # | Secret Name | Value | Source |
|---|---|---|---|
| 1 | `AWS_ACCESS_KEY_ID` | [from AWS setup] | AWS IAM |
| 2 | `AWS_SECRET_ACCESS_KEY` | [from AWS setup] | AWS IAM |
| 3 | `EC2_HOST` | `203.0.113.45` | EC2 instance |
| 4 | `EC2_USER` | `ubuntu` | ✅ Ready (see above) |
| 5 | `EC2_PRIVATE_KEY` | [from above] | ✅ Ready (see above) |

---

## ✅ Verification Checklist

Before moving to deployment:

- [ ] SSH keys generated ✅
- [ ] AWS setup completed
  - [ ] ECR repository created
  - [ ] IAM user created
  - [ ] Access keys generated
- [ ] EC2 instance launched
  - [ ] Docker installed
  - [ ] Security group configured (ports 22, 80, 443)
- [ ] All 5 secrets added to GitHub
  - [ ] AWS_ACCESS_KEY_ID
  - [ ] AWS_SECRET_ACCESS_KEY
  - [ ] EC2_HOST
  - [ ] EC2_USER
  - [ ] EC2_PRIVATE_KEY

---

## 📝 Next Steps

1. Add public key to EC2:
   ```bash
   ssh -i /path/to/your/ec2/key.pem ubuntu@YOUR_EC2_IP
   mkdir -p ~/.ssh
   cat >> ~/.ssh/authorized_keys << 'EOF'
   ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC/lrhkXkwT9DFRBm0l2UcMY7/5roWQlVWn72VHjTbPdEUB3Xfs4GYp9Vf4nhfqFeSUubK0NRFnPfcy+5DnWqrdxGIOpbe7nK6enxUOZLox/2/4KsV2P3DqLGnqwksrrfnz7yokPTuJycQHEQ7kxvmtlOxRSLxnukrmUE9lJDCQUMcMGxE33NjURkUvUahpiliJO3tnvY8yPqyiNp/1ABMMh2GQ4mYAZGb9l58rw6wPepDa55GNMyCFNwsAB3QtGGx49Ge+eF8JcQLs6O0Qb6SDBjLzrhXtIFqHCygF7Vyuarmgd0zQCxnwiE5zpnaI1gwvj+srAOtLfV3fZeh7rqSAAXkelRNjmaRB9N2+ZC5ovsx2h5dNRVCkfGHLEichs0ah3deHRAk/NPfqPeeImu6muRj+CKvEbPj7eP97uu8nlKN9n68I3h+gtwTbbKyXrUzQiptIhZ/TmvhSA2OXlW8/bRoJ7Wlkn1luOKUFj7QYnATFdLPR5hvFF3zKP7un7sVNlXU+/Tc9Y1fKL17IyoK5osFCMRBLGJT4L94ONJ+P9MlutQyIvMcCNrwFgNfE/5D405cATrIKe9Qs1PidX5XA80ABtCtgQa7uT+qHL1rDKDN7mA6z4Q91bXhhltuYtpNXhG9TijY5zcLaZMkitRGYcYFT7RUDjgZ3Kn0Ij196QQ== github-actions
   EOF
   ```

2. Commit the workflow files and push to GitHub

3. Watch deployment in GitHub Actions tab

---

## 🆘 Troubleshooting

**"Secret not found" error in workflow:**
- Verify secret name matches exactly (case-sensitive)
- Check secret was saved properly in GitHub
- Refresh browser and try again

**"Permission denied (publickey)":**
- Public key not added to EC2 ~/.ssh/authorized_keys
- Wrong EC2_USER (check if it's "ubuntu", "ec2-user", etc.)
- Private key format incorrect (check BEGIN/END markers preserved)

**AWS credentials not working:**
- Verify access key ID format (starts with AKIA)
- Verify IAM user has ECR permissions
- Check AWS region matches ECR repository region

