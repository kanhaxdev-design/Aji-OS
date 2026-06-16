# Aji OS v1.0 - Deployment Guide

## 🚀 Production Deployment

### Local Development

See [QUICKSTART.md](./QUICKSTART.md) for local setup.

### Web Server Deployment

#### Option 1: Traditional Server (Recommended for production)

**1. Setup Server**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.13 python3-pip nodejs npm
```

**2. Clone Repository**
```bash
git clone https://github.com/kanhaxdev-design/Aji-OS.git
cd Aji-OS
```

**3. Backend Setup**
```bash
cd backend
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with production values
```

**4. Frontend Build**
```bash
cd ../frontend
npm install
npm run build
# Output: frontend/dist/
```

**5. Systemd Service (Linux)**

Create `/etc/systemd/system/aji-os.service`:
```ini
[Unit]
Description=Aji OS Backend Service
After=network.target

[Service]
Type=simple
User=aji
WorkingDirectory=/home/aji/Aji-OS/backend
ExecStart=/home/aji/Aji-OS/backend/venv/bin/python main.py
Restart=always
RestartSec=10
Environment="PATH=/home/aji/Aji-OS/backend/venv/bin"
EnvironmentFile=/home/aji/Aji-OS/backend/.env

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable aji-os
sudo systemctl start aji-os
```

**6. Nginx Reverse Proxy**

Create `/etc/nginx/sites-available/aji-os`:
```nginx
upstream backend {
    server localhost:8000;
}

server {
    listen 80;
    server_name aji-os.yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name aji-os.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/aji-os.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/aji-os.yourdomain.com/privkey.pem;

    # Frontend
    location / {
        root /home/aji/Aji-OS/frontend/dist;
        try_files $uri /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket
    location /ws {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_buffering off;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/aji-os /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**7. SSL Certificate (Let's Encrypt)**
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d aji-os.yourdomain.com
```

#### Option 2: Docker Deployment

**Dockerfile (backend)**
```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

EXPOSE 8000

CMD ["python", "main.py"]
```

**Dockerfile (frontend)**
```dockerfile
FROM node:18-alpine as builder

WORKDIR /app

COPY frontend/package*.json .
RUN npm install

COPY frontend/ .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**docker-compose.yml**
```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - BACKEND_HOST=0.0.0.0
      - BACKEND_PORT=8000
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: always

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - /etc/letsencrypt:/etc/letsencrypt
    depends_on:
      - backend
      - frontend
    restart: always
```

Deploy:
```bash
docker-compose up -d
```

#### Option 3: Cloud Platforms

**Heroku**
```bash
heroku login
heroku create aji-os
heroku config:set GROQ_API_KEY=your_key
git push heroku main
```

**AWS (Elastic Beanstalk)**
```bash
eb init aji-os
eb create aji-os-env
eb deploy
```

**Google Cloud (App Engine)**
```bash
gcloud app deploy
```

**DigitalOcean (App Platform)**
```bash
doctl apps create --spec app.yaml
```

### Desktop Application Distribution

**Build installers:**
```bash
cd src-tauri
cargo tauri build --release
```

**Outputs:**
- Windows: `target/release/bundle/msi/Aji_OS_1.0.0_x64.msi`
- macOS: `target/release/bundle/dmg/Aji OS_1.0.0.dmg`
- Linux: `target/release/bundle/deb/aji-os_1.0.0_amd64.deb`

**Distribution:**
1. Create GitHub releases
2. Upload installers
3. Enable auto-updates in Tauri config
4. Distribute via website/app store

### Monitoring & Maintenance

**Logs**
```bash
# Backend logs
tail -f /var/log/aji-os/backend.log

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

**Health Check**
```bash
curl https://aji-os.yourdomain.com/health
```

**Restart Service**
```bash
sudo systemctl restart aji-os
```

**Backup Data**
```bash
tar -czf backup.tar.gz data/ logs/
```

## 🔧 Performance Tuning

### Backend
```python
# config.py - Adjust for your server
WORKERS = 4  # Number of CPU cores
WORKER_CONNECTIONS = 1000
```

### Frontend
```bash
# Enable gzip compression
gzip on;
gzip_types text/plain application/json;
```

### Database
```bash
# Optimize SQLite
VACUUM;
ANALYZE;
```

## 🔒 Security Checklist

- [ ] SSL/TLS enabled
- [ ] API keys in environment variables
- [ ] CORS configured
- [ ] Rate limiting enabled
- [ ] Input validation active
- [ ] Error logging configured
- [ ] Backups scheduled
- [ ] Monitoring enabled
- [ ] Firewall configured
- [ ] Regular updates applied

## 📊 Scaling

### Horizontal Scaling
1. Load balancer (nginx/HAProxy)
2. Multiple backend instances
3. Shared database
4. Session persistence

### Vertical Scaling
1. Increase server resources
2. Optimize database queries
3. Enable caching
4. Use CDN for frontend

## 🆘 Troubleshooting

**API returns 502 Bad Gateway**
- Check backend is running: `systemctl status aji-os`
- Check Nginx proxy settings
- Review backend logs

**High memory usage**
- Monitor with `top` or `htop`
- Check for memory leaks in code
- Increase swap space

**Database locked errors**
- SQLite has limited concurrency
- Consider PostgreSQL for production
- Enable WAL mode: `PRAGMA journal_mode=WAL;`

---

For more help, see [SETUP.md](./SETUP.md) and [CONTRIBUTING.md](./CONTRIBUTING.md)
