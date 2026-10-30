# Production & Ngrok Settings Guide for Proxmox (LXC / VM)

### 1. Requirements on Proxmox LXC/VM (Ubuntu/Debian)
```bash
sudo apt update && sudo apt install -y python3 python3-pip python3-venv git curl
```

### 2. Ngrok Authtoken & Reserved Domain (Recommended)
Free Ngrok accounts can claim 1 permanent static domain (e.g. `your-domain.ngrok-free.app`):
```bash
# Install ngrok
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
  | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
  && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
  | sudo tee /etc/apt/sources.list.d/ngrok.list \
  && sudo apt update && sudo apt install ngrok

# Authenticate
ngrok config add-authtoken <YOUR_NGROK_TOKEN>
```

### 3. Running Backend 24/7 via PM2
File konfigurasi `ecosystem.config.js` sudah disiapkan di root folder:
```bash
# Install PM2 jika belum
sudo npm install -g pm2

# Start Django backend dan Ngrok bersamaan
pm2 start ecosystem.config.js

# Simpan state agar autostart saat VM/LXC reboot
pm2 save
pm2 startup
```

**Cek status & URL Ngrok:**
```bash
pm2 status
pm2 logs epub-ngrok
# Atau curl endpoint internal ngrok:
curl -s http://127.0.0.1:4040/api/tunnels | grep -o 'https://[^"]*ngrok[^"]*'
```

### 4. GitHub Actions Deployment
In your GitHub repo:
1. Go to **Settings > Secrets and variables > Actions**.
2. Add Repository secret:
   - Name: `VITE_API_URL`
   - Value: `https://your-domain.ngrok-free.app` (or your current Ngrok URL)
3. Push to `main` branch. GitHub Actions will build and deploy your React app automatically to GitHub Pages!

### Credits & Acknowledgements
- UI Card Layout & Aesthetic adapted from [lara-novelku](https://github.com/taufiq-azr/lara-novelku) by [@taufiq-azr](https://github.com/taufiq-azr).


