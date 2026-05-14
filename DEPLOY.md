# Deploy to Render

## Option 1: Blueprint Deploy (Easiest)

1. Push code to GitHub
2. Go to [dashboard.render.com/blueprints](https://dashboard.render.com/blueprints)
3. Connect your repo
4. Render reads `render.yaml` and creates everything automatically

## Option 2: Manual Setup

### Create Services:

1. **PostgreSQL**
   - New → PostgreSQL
   - Name: `leadgen-db`
   - Plan: Free
   - Copy the "Internal Database URL"

2. **Redis**
   - New → Redis
   - Name: `leadgen-redis`
   - Plan: Free
   - Copy the "Internal Redis URL"

3. **Web Service**
   - New → Web Service
   - Connect your repo
   - Runtime: Docker
   - Plan: Free
   - Environment Variables:
     ```
     DATABASE_URL=postgresql+asyncpg://... (from step 1)
     REDIS_URL=redis://... (from step 2)
     SECRET_KEY=generate-a-random-string
     DEBUG=false
     APP_URL=https://your-service-name.onrender.com
     ```

## Custom Domain (Optional)

1. In Render dashboard → your web service → Settings → Custom Domain
2. Add your domain (e.g., `leads.yourcompany.com`)
3. Add CNAME record pointing to Render
4. SSL auto-provisions

## Free Tier Limits

- Web: 512 MB RAM, sleeps after 15 min inactivity (wakes on request)
- Postgres: 1 GB storage, shared CPU
- Redis: 25 MB, shared CPU

**For 3 users, this is plenty.**

## Upgrade When Needed

| Plan | Cost | When to Upgrade |
|------|------|----------------|
| Starter | $7/mo | Need always-on |
| Standard | $25/mo | More RAM/CPU |
| Pro | $85/mo | Production workload |

---

## Alternative: Self-Host on Hetzner ($5/mo)

If you want full control and always-on:

```bash
# 1. Create VPS (CX11 - 1 vCPU, 2 GB RAM, $4.51/mo)
# 2. SSH in and run:

curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker

git clone https://github.com/YOUR_USER/b2b-lead-gen.git
cd b2b-lead-gen
cp .env.example .env
# Edit .env with your settings

docker-compose up -d
```

Add Cloudflare (free) for SSL + CDN in front.

**Total: ~$5/mo for always-on, full control.**
