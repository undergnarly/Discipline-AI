# 🚀 AI-Powered Productivity Tracker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-15+-black.svg)](https://nextjs.org)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org)

> Твой персональный AI-ассистент для продуктивности с Pomodoro, Google Calendar и умным планированием

## ✨ Возможности

- 📅 **Google Calendar Integration** - двусторонняя синхронизация
- ⏰ **Pomodoro Tracker** - с обязательной рефлексией после каждой сессии
- 🤖 **AI Chat** - голосовой и текстовый ассистент на Claude
- 📊 **Analytics** - semantic search по всей истории задач
- 🎯 **Smart Planning** - AI рекомендации на основе паттернов
- 💬 **Voice Notes** - быстрые голосовые команды
- 📈 **Statistics** - визуализация продуктивности

## 🏗️ Архитектура

### Backend
- **FastAPI** - современный async Python фреймворк
- **PostgreSQL + SQLite** - гибкая база данных
- **LangGraph** - multi-agent AI система
- **Claude Sonnet 4** - основной AI модель
- **OpenAI Whisper** - speech-to-text

### Frontend
- **Next.js 15** - React framework с App Router
- **TypeScript** - типизация
- **Tailwind CSS** - стилизация
- **Zustand** - state management
- **FullCalendar** - календарь

### AI Agents
1. **Supervisor Agent** - диспетчер всех агентов
2. **Calendar Agent** - управление календарем
3. **Reflection Agent** - анализ рефлексий
4. **Search Agent** - semantic search
5. **Planning Agent** - помощь в планировании
6. **Insight Agent** - аналитика и рекомендации

## 🚀 Быстрый старт

### Локальная разработка

```bash
# Клонировать репозиторий
git clone https://github.com/undergnarly/Discipline-AI.git
cd Discipline-AI

# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (новый терминал)
cd frontend
npm install
npm run dev
```

Открой в браузере:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📦 Развертывание на сервере

Подробная инструкция в [SERVER_DEPLOYMENT.md](SERVER_DEPLOYMENT.md)

Краткая версия:

```bash
# 1. SSH на сервер
ssh root@64.225.113.174

# 2. Клонировать репозиторий
cd /var/www
git clone https://github.com/undergnarly/Discipline-AI.git
cd Discipline-AI

# 3. Запустить скрипты настройки
chmod +x setup-server.sh && ./setup-server.sh
chmod +x init-backend.sh && ./init-backend.sh
chmod +x init-frontend.sh && ./init-frontend.sh
chmod +x setup-nginx.sh && ./setup-nginx.sh
```

## 🔧 Конфигурация

### Backend (.env)

```env
DATABASE_URL=sqlite+aiosqlite:///./discipline_ai.db
SECRET_KEY=your_secret_key
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📚 Документация

- [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) - Полная спецификация продукта
- [SERVER_DEPLOYMENT.md](SERVER_DEPLOYMENT.md) - Инструкция по развертыванию
- [DEPLOYMENT.md](DEPLOYMENT.md) - Детальное руководство по деплою
- [QUICK_START.md](QUICK_START.md) - Quick start guide

## 🛠️ Технологический стек

| Категория | Технология |
|-----------|------------|
| Backend | FastAPI, Python 3.11+ |
| Frontend | Next.js 15, React 19, TypeScript |
| Database | PostgreSQL, SQLite |
| AI | Claude Sonnet 4, LangGraph |
| Voice | OpenAI Whisper |
| Calendar | Google Calendar API |
| Styling | Tailwind CSS |
| State | Zustand |
| Charts | Recharts |
| Calendar UI | FullCalendar |

## 🗺️ Roadmap

### Phase 1: Foundation ✅
- [x] Базовая архитектура
- [x] JWT Auth
- [x] Google OAuth
- [x] Базовый calendar

### Phase 2: Core Features (в процессе)
- [ ] Pomodoro Tracker с рефлексией
- [ ] AI Chat с голосом
- [ ] FullCalendar интеграция
- [ ] Semantic search

### Phase 3: Advanced Features
- [ ] Multi-agent система
- [ ] Advanced analytics
- [ ] Smart notifications
- [ ] Mobile PWA

## 🤝 Вклад в развитие

1. Fork репозиторий
2. Создай feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add some AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Открой Pull Request

## 📝 Лицензия

Этот проект лицензирован под MIT License - смотри [LICENSE](LICENSE) файл для деталей

## 👨‍💻 Автор

**undergnarly**

- GitHub: [@undergnarly](https://github.com/undergnarly)

## 🙏 Благодарности

- [FastAPI](https://fastapi.tiangolo.com) - Современный Python web framework
- [Next.js](https://nextjs.org) - React framework
- [Anthropic](https://www.anthropic.com) - Claude AI
- [Vercel](https://vercel.com) - Next.js deployment

---

⭐ Если этот проект был полезен, поставь звезду!

📧 Контакты: Создай issue на GitHub для вопросов и предложений
