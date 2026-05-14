# Deploy to Render

## ⚠️ Current Issue: Render Builds Failing

The automatic API deployment is failing. Use the **manual dashboard setup** instead.

## Manual Setup (Recommended)

### Step 1: Create Services on Render Dashboard

1. Go to [dashboard.render.com](https://dashboard.render.com)

2. **Create PostgreSQL**
   - New + → PostgreSQL
   - Name: `leadgen-db`
   - Plan: Free
   - Database: `leadgen`
   - User: `leadgen`
   - Click "Create Database"
   - **Copy the "Internal Database URL"**

3. **Create Redis**
   - New + → Redis
   - Name: `leadgen-redis`
   - Plan: Free
   - Click "Create Redis"
   - **Copy the "Internal Redis URL"**

4. **Create Web Service**
   - New + → Web Service
   - Connect your GitHub repo: `xyncblock/b2b-lead-gen`
   - Name: `b2b-lead-gen`
   - Region: Oregon (or closest to you)
   - Branch: `master`
   - Runtime: **Python 3**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - Plan: Free
   - Click "Create Web Service"

### Step 2: Add Environment Variables

In the Web Service dashboard, go to "Environment" tab and add:

```
DATABASE_URL=postgresql+asyncpg://... (from step 1 - use the internal URL)
REDIS_URL=redis://... (from step 2 - use the internal URL)
SECRET_KEY=your-random-secret-key-here
DEBUG=false
APP_URL=https://b2b-lead-gen.onrender.com
```

### Step 3: Deploy

Click "Manual Deploy" → "Deploy latest commit"

Wait 2-3 minutes for the build to complete.

### Step 4: Verify

Visit: `https://b2b-lead-gen.onrender.com/health/live`

Should return: `{"status":"alive","version":"1.0.0","timestamp":"..."}`

---

## Alternative: Hetzner VPS ($5/mo)

If Render keeps failing, a VPS gives you full control:

```bash
# 1. Create CX11 instance on Hetzner Cloud (~$4.51/mo)
# 2. SSH into server

# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker

# Clone repo
git clone https://github.com/xyncblock/b2b-lead-gen.git
cd b2b-lead-gen

# Create .env file
cat > .env << 'EOF'
DATABASE_URL=postgresql+asyncpg://leadgen:password@db:5432/leadgen
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-secret-key-here
DEBUG=false
APP_URL=http://your-server-ip:8000
EOF

# Run with Docker Compose
docker-compose up -d

# Setup SSL with Caddy or Nginx (optional)
```

---

## Current Status

- ✅ GitHub repo: https://github.com/xyncblock/b2b-lead-gen
- ✅ PostgreSQL DB: Created on Render
- ✅ Redis: Created on Render
- ❌ Web Service: Build failures via API
- 🔄 Next: Manual dashboard setup required
