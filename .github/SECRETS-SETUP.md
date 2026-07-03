# GitHub Secrets Configuration Template

This file documents all required GitHub Secrets for the deployment workflows.

**Location:** Repository → Settings → Secrets and variables → Actions

---

## For ECR-based deployment (deploy-to-ec2.yml)

Required secrets:

### 1. AWS_ACCESS_KEY_ID
**Source:** IAM User credentials
**How to get:**
1. AWS Console → IAM → Users
2. Create user: `github-actions-deploy`
3. Security credentials → Create access key
4. Copy the "Access key ID"

**Format:** Plain text alphanumeric
**Example:** `AKIA1234567890ABCDEF`

---

### 2. AWS_SECRET_ACCESS_KEY
**Source:** IAM User credentials (same as above)
**How to get:**
1. From same IAM user creation (Step 1-3 above)
2. Copy the "Secret access key"

**Format:** Plain text (can contain special characters)
**Example:** `wJaP+xB9...` (40+ characters)

**⚠️ CRITICAL:** This is secret - save it immediately, cannot be retrieved later

---

### 3. EC2_HOST
**Source:** Your EC2 instance
**How to get:**
1. AWS Console → EC2 → Instances
2. Select your instance
3. Copy "Public IPv4 address" OR "Public IPv4 DNS"

**Format:** IP address or domain name
**Examples:**
- `203.0.113.45` (Public IP)
- `ec2-203-0-113-45.compute-1.amazonaws.com` (Public DNS)
- `dashboard.yourdomain.com` (Custom domain)

---

### 4. EC2_USER
**Source:** Your EC2 instance operating system
**How to get:**
1. Based on your AMI OS:
   - Ubuntu: `ubuntu`
   - Amazon Linux 2: `ec2-user`
   - CentOS: `centos`

**Format:** Plain text username
**Example:** `ubuntu`

---

### 5. EC2_PRIVATE_KEY
**Source:** SSH key pair you created
**How to get:**
1. Generate SSH key on your computer:
   ```bash
   ssh-keygen -t rsa -b 4096 -f github-deploy-key -C "github-actions"
   ```
2. Open the private key file: `github-deploy-key`
3. Copy entire contents (including `-----BEGIN RSA PRIVATE KEY-----` and `-----END RSA PRIVATE KEY-----`)

**Format:** Multi-line PEM format
**Example:**
```
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA2x3Z8q+vE9K...
[many lines]
...1wZXQx0QIDAQABAoIBAAxyz123...
-----END RSA PRIVATE KEY-----
```

**⚠️ CRITICAL:** Keep this private - never commit to git or share

**How to add multi-line secret to GitHub:**
1. Go to GitHub Secrets page
2. Click "New repository secret"
3. Name: `EC2_PRIVATE_KEY`
4. In Value field, paste entire key contents (including BEGIN/END lines)
5. GitHub will automatically preserve newlines

---

## For Simple deployment (deploy-to-ec2-simple.yml)

Only requires 3 secrets (no AWS credentials):

1. **EC2_HOST** - (see above)
2. **EC2_USER** - (see above)
3. **EC2_PRIVATE_KEY** - (see above)

---

## Verification Checklist

- [ ] AWS_ACCESS_KEY_ID: 20 character alphanumeric starting with "AKIA"
- [ ] AWS_SECRET_ACCESS_KEY: 40+ character string with special characters
- [ ] EC2_HOST: Valid IP (xxx.xxx.xxx.xxx) or domain name
- [ ] EC2_USER: Matches your EC2 OS (ubuntu, ec2-user, etc)
- [ ] EC2_PRIVATE_KEY: Full private key with BEGIN/END markers

---

## Testing Secrets

After adding secrets, verify they work:

```bash
# Test SSH key
ssh -i github-deploy-key ubuntu@YOUR_EC2_HOST "echo 'Connection successful!'"

# Test AWS credentials (from your computer with AWS CLI)
export AWS_ACCESS_KEY_ID="your_key_id"
export AWS_SECRET_ACCESS_KEY="your_secret"
aws ecr describe-repositories --region us-east-1
```

---

## Rotating/Updating Secrets

### Update AWS Credentials
1. AWS IAM Console
2. Delete old access key
3. Generate new access key
4. Update both `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` on GitHub

### Update SSH Keys
1. Generate new key pair: `ssh-keygen -t rsa -b 4096 -f github-deploy-key`
2. Add public key to EC2: `cat github-deploy-key.pub >> ~/.ssh/authorized_keys`
3. Update `EC2_PRIVATE_KEY` on GitHub

### Update EC2 Host
1. If EC2 IP changed, update `EC2_HOST`
2. Regenerate SSH keys if using new EC2 instance

---

## Troubleshooting Secrets

### "Permission denied (publickey)"
- EC2_PRIVATE_KEY format incorrect (missing newlines or markers)
- Public key not added to EC2 ~/.ssh/authorized_keys
- EC2_USER doesn't match actual SSH user

### "Access Denied" on AWS operations
- AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY incorrect
- IAM user doesn't have required permissions
- Credentials don't match the AWS region

### Secret not working in workflow
- GitHub secrets are case-sensitive
- Whitespace might be included (avoid copy-paste from word processors)
- Secret hasn't been saved yet (refresh page)

---

## Security Best Practices

✓ Never commit secrets to git
✓ Don't share secrets in emails or chat
✓ Rotate credentials every 90 days
✓ Delete old/unused access keys
✓ Use strong, unique passphrases for SSH keys
✓ Restrict IAM user to minimum required permissions
✓ Enable MFA on AWS account
✓ Monitor CloudTrail for suspicious activity

