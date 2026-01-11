# 🚀 Deployment Guide - Server 64.225.113.174

## 📋 Подготовка к развертыванию

### Шаг 1: Создать GitHub репозиторий и запушить код

**На локальной машине:**

```bash
cd /home/muvs/pets/discipline-ai-new

# Добавить все файлы в git
git add .

# Сделать первый коммит
git commit -m "Initial commit: Discipline AI Productivity Tracker"

# Создать репозиторий на GitHub:
# 1. Зайди на https://github.com/new
# 2. Создай новый репозиторий "discipline-ai"
# 3. Не отмечай "Add a README file" (уже есть)
# 4. Нажми "Create repository"

# После создания GitHub репозитория, выполни:
git remote add origin https://github.com/ТВОЙ_ЮЗЕРНЕЙМ/discipline-ai.git
git branch -M main
git push -u origin main
```

---

## 🖥️ Развертывание на сервере 64.225.113.174

### Шаг 2: Подключиться к серверу

```bash
# Если у тебя есть SSH ключ
ssh root@64.225.113.174

# Или если нужен пароль
ssh root@64.225.113.174
```

### Шаг 3: Установить необходимое ПО на сервере

**После подключения к серверу:**

```bash
# Обновить систему
apt update && apt upgrade -y

# Установить Python 3.11+
apt install -y python3.11 python3.11-venv python3-pip

# Установить Node.js 20.x
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs

# Установить Nginx
apt install -y nginx

# Установить PM2 (для запуска Node.js приложений в production)
npm install -g pm2

# Установить Git
apt install -y git

# Проверить версии
python3.11 --version
node --version
npm --version
git --version
```

### Шаг 4: Клонировать репозиторий

```bash
# Создать директорию для проекта
mkdir -p /var/www
cd /var/www

# Клонировать репозиторий (замени на свой GitHub URL)
git clone https://github.com/ТВОЙ_ЮЗЕРНЕЙМ/discipline-ai.git
cd discipline-ai
```

### Шаг 5: Настроить Backend

```bash
# Перейти в backend директорию
cd /var/www/discipline-ai/backend

# Создать виртуальное окружение
python3.11 -m venv venv

# Активировать виртуальное окружение
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Создать production .env файл
cat > .env << 'EOF'
# Database (SQLite для начала)
DATABASE_URL=sqlite+aiosqlite:///./discipline_ai.db

# JWT (Смени на безопасные значения!)
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
FRONTEND_URL=https:// discipline-ai.com

# Google OAuth (добавь позже)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=https://discipline-ai.com/api/auth/google/callback

# OpenAI (добавь позже)
OPENAI_API_KEY=

# Anthropic (добавь позже)
ANTHROPIC_API_KEY=

# Supabase (добавь позже)
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
EOF

# Создать базу данных и миграции
alembic upgrade head
```

### Шаг 6: Настроить Frontend

```bash
# Перейти в frontend директорию
cd /var/www/discipline-ai/frontend

# Установить зависимости
npm install

# Создать production build
npm run build

# Создать .env.local для production
cat > .env.local << 'EOF'
NEXT_PUBLIC_API_URL=https://discipline-ai.com/api
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
EOF
```

### Шаг 7: Настроить Systemd для Backend

```bash
# Создать systemd service файл для backend
cat > /etc/systemd/system/discipline-ai-backend.service << 'EOF'
[Unit]
Description=Discipline AI Backend FastAPI
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/discipline-ai/backend
Environment="PATH=/var/www/discipline-ai/backend/venv/bin"
ExecStart=/var/www/discipline-ai/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Включить и запустить backend service
systemctl daemon-reload
systemctl enable discipline-ai-backend
systemctl start discipline-ai-backend

# Проверить статус
systemctl status discipline-ai-backend
```

### Шаг 8: Настроить PM2 для Frontend

```bash
# Запустить Next.js в production режиме с PM2
cd /var/www/discipline-ai/frontend
pm2 start npm --name "discipline-ai-frontend" -- start

# Сохранить PM2 configuration
pm2 save

# Настроить PM2 для автозапуска при загрузке
pm2 startup
# Выполнить команду, которую покажет PM2

# Проверить статус
pm2 status
pm2 logs discipline-ai-frontend
```

### Шаг 9: Настроить Nginx

```bash
# Создать Nginx конфигурацию
cat > /etc/nginx/sites-available/discipline-ai << 'EOF'
server {
    listen 80;
    server_name discipline-ai.com www.discipline-ai.com;

    # Frontend (Next.js)
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API Docs (Swagger UI) - опционально, можно отключить в production
    location /docs {
        proxy_pass http://localhost:8000/docs;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Включить сайт
ln -s /etc/nginx/sites-available/discipline-ai /etc/nginx/sites-enabled/

# Удалить default конфиг (опционально)
rm -f /etc/nginx/sites-enabled/default

# Проверить конфигурацию Nginx
nginx -t

# Перезапустить Nginx
systemctl restart nginx
```

### Шаг 10: Настроить Firewall

```bash
# Разрешить HTTP и HTTPS
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 22/tcp
ufw enable

# Проверить статус
ufw status
```

### Шаг 11: Настроить SSL с Let's Encrypt (HTTPS)

```bash
# Установить Certbot
apt install -y certbot python3-certbot-nginx

# Получить SSL сертификат
certbot --nginx -d discipline-ai.com -d www.discipline-ai.com

# Certbot автоматически настроит Nginx для HTTPS

# Проверить автозапуск сертификата
certbot renew --dry-run
```

---

## 🔄 Обновление приложения

Когда нужно обновить код на сервере:

```bash
# SSH на сервер
ssh root@64.225.113.174

# Перейти в директорию проекта
cd /var/www/discipline-ai

# Подтянуть изменения из GitHub
git pull origin main

# Обновить backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
systemctl restart discipline-ai-backend

# Обновить frontend
cd ../frontend
npm install
npm run build
pm2 restart discipline-ai-frontend
```

---

## 📊 Мониторинг

### Проверить логи:

```bash
# Backend logs
journalctl -u discipline-ai-backend -f

# Frontend logs
pm2 logs discipline-ai-frontend

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Проверить статус сервисов:

```bash
# Backend
systemctl status discipline-ai-backend

# Frontend
pm2 status

# Nginx
systemctl status nginx
```

---

## 🔐 Безопасность

1. **Изменить SECRET_KEY в .env** на случайное значение
2. **Настроить firewall** - оставить только необходимые порты
3. **Использовать HTTPS** - Let's Encrypt бесплатный
4. **Регулярно обновлять сервер** - `apt update && apt upgrade`
5. **Настроить автоматические бэкапы** базы данных
6. **Ограничить доступ по SSH** - только ключи, отключить пароль

---

## 🌐 DNS Настройки

Добавить A записи в настройках домена:

```
Type: A
Name: @
Value: 64.225.113.174
TTL: 3600

Type: A
Name: www
Value: 64.225.113.174
TTL: 3600
```

---

## 📝 Следующие шаги после развертывания:

1. **Добавить API ключи** в .env файлы:
   - Google OAuth (CLIENT_ID, CLIENT_SECRET)
   - OpenAI API Key
   - Anthropic API Key
   - Supabase credentials

2. **Настроить базу данных PostgreSQL** (вместо SQLite для production)

3. **Настроить CI/CD** для автоматического деплоя из GitHub

4. **Добавить мониторинг** (Sentry, LogRocket, etc.)

5. **Настроить бэкапы** базы данных

---

**Создано:** 2026-01-11
**Статус:** Готово к развертыванию
