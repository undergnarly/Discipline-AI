# 🚀 AI-Powered Productivity Tracker - Implementation Plan

## 📋 Текущее состояние проекта

**Что уже есть:**
- ✅ FastAPI backend с JWT auth
- ✅ Next.js 14 frontend с TypeScript
- ✅ PostgreSQL + SQLAlchemy async
- ✅ Google OAuth базовая интеграция
- ✅ Docker Compose конфигурация
- ✅ Базовые модели User и CalendarEvent

**Что нужно создать (по новой спецификации):**
- ❌ Pomodoro Tracker с рефлексией
- ❌ AI Chat (голос + текст)
- ❌ FullCalendar интеграция
- ❌ Reports & Analytics с semantic search
- ❌ Dashboard с morning briefing
- ❌ Statistics визуализация
- ❌ LangGraph Multi-Agent система
- ❌ Supabase интеграция (вместо текущего PostgreSQL)

---

## 🎯 Новая архитектура (Target)

### Tech Stack Changes

**Frontend:**
- Next.js 15 (App Router) [обновить с 14]
- Zustand (state management) [вместо React Query]
- shadcn/ui + Tailwind [уже есть Tailwind]
- FullCalendar + Google Calendar plugin [новое]
- Recharts [новое]

**Backend:**
- FastAPI [остается]
- LangGraph для multi-agent системы [новое]
- Claude Sonnet 4 [новое - вместо OpenAI]
- OpenAI Whisper для STT [новое]
- OpenAI embeddings [новое]

**Database:**
- Supabase (PostgreSQL + pgvector) [НОВОЕ - миграция с pure PostgreSQL]
- Row Level Security
- Realtime subscriptions

---

## 📊 Database Schema (Новый)

### 1. profiles
```sql
CREATE TABLE profiles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  avatar TEXT,
  google_calendar_id TEXT,
  google_refresh_token TEXT,
  preferences JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 2. tasks (заменяет calendar_events)
```sql
CREATE TABLE tasks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  description TEXT,
  start_time TIMESTAMPTZ,
  end_time TIMESTAMPTZ,
  status TEXT DEFAULT 'pending', -- pending, in_progress, completed, cancelled
  google_event_id TEXT UNIQUE,
  tags TEXT[] DEFAULT '{}',
  priority INTEGER DEFAULT 1, -- 1-5
  project TEXT,
  energy_level INTEGER, -- 1-5, после завершения
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 3. pomodoro_sessions
```sql
CREATE TABLE pomodoro_sessions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  task_id UUID REFERENCES tasks(id) ON DELETE SET NULL,
  duration INTEGER NOT NULL, -- минут
  started_at TIMESTAMPTZ DEFAULT NOW(),
  ended_at TIMESTAMPTZ,
  reflection_text TEXT,
  reflection_challenges TEXT,
  notes_for_future TEXT,
  action_taken TEXT, -- continue, complete, postpone
  ai_summary TEXT,
  ai_insights JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 4. chat_messages
```sql
CREATE TABLE chat_messages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  role TEXT NOT NULL, -- user, assistant, system
  content TEXT NOT NULL,
  is_voice BOOLEAN DEFAULT FALSE,
  audio_url TEXT,
  task_id UUID REFERENCES tasks(id) ON DELETE SET NULL,
  session_id UUID REFERENCES pomodoro_sessions(id) ON DELETE SET NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 5. daily_reports
```sql
CREATE TABLE daily_reports (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  date DATE UNIQUE NOT NULL,
  total_pomodoros INTEGER DEFAULT 0,
  total_minutes INTEGER DEFAULT 0,
  completed_tasks INTEGER DEFAULT 0,
  deep_work_minutes INTEGER DEFAULT 0,
  ai_summary TEXT,
  insights JSONB DEFAULT '{}',
  streak_days INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 6. task_embeddings (для AI search)
```sql
CREATE TABLE task_embeddings (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  content TEXT NOT NULL,
  embedding vector(1536), -- OpenAI embedding dimension
  task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
  session_id UUID REFERENCES pomodoro_sessions(id) ON DELETE CASCADE,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
-- CREATE INDEX ON task_embeddings USING ivfflat (embedding vector_cosine_ops);
```

### 7. user_streaks
```sql
CREATE TABLE user_streaks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE UNIQUE,
  current_streak INTEGER DEFAULT 0,
  longest_streak INTEGER DEFAULT 0,
  last_pomodoro_date DATE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 🤖 LangGraph Multi-Agent System

### Agent Architecture

```
User Request
    ↓
Supervisor Agent (диспетчер)
    ↓
    ├──→ Calendar Agent (управление событиями)
    ├──→ Reflection Agent (анализ рефлексий)
    ├──→ Search Agent (semantic search)
    ├──→ Planning Agent (помощь в планировании)
    └──→ Insight Agent (аналитика и рекомендации)
```

### 1. Supervisor Agent
**Файл:** `backend/app/agents/supervisor.py`

**Responsibilities:**
- Анализирует запрос пользователя
- Определяет какой агент нужен
- Маршрутизирует запрос
- Агрегирует результаты

**State Schema:**
```python
class SupervisorState(TypedDict):
    messages: List[BaseMessage]
    next_agent: str
    user_context: dict
    calendar_context: dict
    result: Optional[str]
```

### 2. Calendar Agent
**Файл:** `backend/app/agents/calendar.py`

**Capabilities:**
- Создание/изменение/удаление событий
- Синхронизация с Google Calendar
- Умное планирование (поиск свободного времени)
- Color coding событий

**Tools:**
- `create_task` - создать задачу
- `update_task` - обновить задачу
- `delete_task` - удалить задачу
- `find_free_slot` - найти свободное время
- `sync_with_google` - синхронизация с Google Calendar

### 3. Reflection Agent
**Файл:** `backend/app/agents/reflection.py`

**Capabilities:**
- Анализ текста после Pomodoro
- Генерация структурированных insights
- Связывание с похожими задачами
- Предложение решений для сложностей

**Tools:**
- `analyze_reflection` - анализ рефлексии
- `find_similar_tasks` - найти похожие задачи
- `generate_insights` - генерация insights
- `suggest_solutions` - предложить решения

### 4. Search Agent
**Файл:** `backend/app/agents/search.py`

**Capabilities:**
- Semantic search через embeddings
- Фильтрация по времени/категориям
- Кросс-референсы между задачами

**Tools:**
- `semantic_search` - семантический поиск
- `filter_by_time` - фильтр по времени
- `filter_by_category` - фильтр по категории
- `find_cross_references` - найти связи

### 5. Planning Agent
**Файл:** `backend/app/agents/planning.py`

**Capabilities:**
- Разбиение больших задач на подзадачи
- Оптимизация расписания
- Приоритизация

**Tools:**
- `break_down_task` - разбить задачу
- `optimize_schedule` - оптимизировать расписание
- `suggest_priority` - предложить приоритет
- `estimate_duration` - оценить длительность

### 6. Insight Agent
**Файл:** `backend/app/agents/insight.py`

**Capabilities:**
- Генерация статистики
- Поиск паттернов
- Персонализированные рекомендации

**Tools:**
- `generate_statistics` - генерация статистики
- `detect_patterns` - обнаружить паттерны
- `generate_recommendations` - генерировать рекомендации
- `compare_periods` - сравнить периоды

---

## 📁 Frontend Structure

### Pages Structure
```
app/
├── (auth)/
│   ├── login/
│   └── register/
├── (app)/
│   ├── layout.tsx (главный layout с sidebar)
│   ├── dashboard/          # Dashboard
│   ├── calendar/           # Calendar (FullCalendar)
│   ├── pomodoro/           # Pomodoro Tracker
│   ├── chat/               # AI Chat
│   ├── reports/            # Reports & Analytics
│   └── statistics/         # Statistics
└── api/                    # API routes (если нужно для Next.js)
```

### Key Components

**1. Dashboard (`app/(app)/dashboard/page.tsx`)**
```tsx
- Morning briefing (AI саммари дня)
- Текущая активная задача (большая карточка)
- Следующие 3 задачи на сегодня
- Streak и статистика
- Quick AI chat
- Mini-график продуктивности (7 дней)
```

**2. Calendar (`app/(app)/calendar/page.tsx`)**
```tsx
- FullCalendar компонент
- Google Calendar plugin
- Drag & drop
- Месяц/Неделя/День виды
- Боковая панель с деталями задачи
- AI chat в контексте задачи
- Heat map mode
- Time boxing assistant
```

**3. Pomodoro (`app/(app)/pomodoro/page.tsx`)**
```tsx
- Выбор задачи из календаря
- Выбор длины (15/25/50 мин)
- Таймер (full screen опционально)
- Форма рефлексии (после завершения)
- Streak система
- Deep work score
```

**4. AI Chat (`app/(app)/chat/page.tsx`)**
```tsx
- Голосовой ввод (Web Speech API / отправка на backend)
- Текстовый ввод
- История сообщений
- Context-aware (если открыта из задачи)
- Proactive suggestions
```

**5. Reports (`app/(app)/reports/page.tsx`)**
```tsx
- AI Search (semantic search)
- Временные фильтры
- Экспорт (PDF, Excel, markdown)
- Кросс-референсы
```

**6. Statistics (`app/(app)/statistics/page.tsx`)**
```tsx
- Recharts графики
- Pomodoro count
- Фактическое vs запланированное
- Completion rate
- Распределение по категориям
- Deep work vs shallow work
- Productivity score
- Compare periods
```

---

## 🔧 Backend API Structure

### Endpoints

**Auth:**
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/google`
- `POST /api/auth/refresh`
- `POST /api/auth/logout`

**Calendar/Tasks:**
- `GET /api/tasks` - список задач
- `POST /api/tasks` - создать задачу
- `GET /api/tasks/{id}` - деталь задачи
- `PUT /api/tasks/{id}` - обновить задачу
- `DELETE /api/tasks/{id}` - удалить задачу
- `POST /api/tasks/sync-google` - синхронизация с Google Calendar

**Pomodoro:**
- `POST /api/pomodoro/start` - начать сессию
- `POST /api/pomodoro/stop` - остановить сессию
- `POST /api/pomodoro/reflection` - отправить рефлексию
- `GET /api/pomodoro/active` - активная сессия
- `GET /api/pomodoro/history` - история сессий

**AI Chat:**
- `POST /api/chat/message` - отправить сообщение
- `POST /api/chat/voice` - отправить голосовое (с audio file)
- `GET /api/chat/history` - история чата
- `DELETE /api/chat/history` - очистить историю

**Reports & Analytics:**
- `POST /api/reports/search` - AI semantic search
- `GET /api/reports/daily/{date}` - дневной отчет
- `GET /api/reports/weekly` - недельный отчет
- `GET /api/reports/export` - экспорт отчета

**Statistics:**
- `GET /api/stats/overview` - общая статистика
- `GET /api/stats/pomodoros` - статистика Pomodoro
- `GET /api/stats/categories` - распределение по категориям
- `GET /api/stats/patterns` - паттерны продуктивности
- `GET /api/stats/productivity-score` - productivity score

**AI Agents:**
- `POST /api/agents/supervisor` - вызвать supervisor agent
- `POST /api/agents/calendar` - вызвать calendar agent
- `POST /api/agents/reflection` - вызвать reflection agent
- `POST /api/agents/search` - вызвать search agent
- `POST /api/agents/planning` - вызвать planning agent
- `POST /api/agents/insight` - вызвать insight agent

---

## 🚀 Implementation Phases

### Phase 1: Foundation & Database Migration (Priority 1)

**Backend:**
1. Setup Supabase project
2. Create database schema (all tables)
3. Implement Row Level Security policies
4. Create migration scripts
5. Setup pgvector extension
6. Update SQLAlchemy models

**Frontend:**
1. Setup shadcn/ui
2. Install dependencies:
   - @fullcalendar/react
   - @fullcalendar/google-calendar
   - zustand
   - recharts
   - framer-motion
3. Create base layout structure
4. Setup Supabase client

---

### Phase 2: Calendar Integration (Priority 1)

**Backend:**
1. Complete Google Calendar API integration
2. Implement bidirectional sync
3. Create calendar endpoints
4. Smart notifications system

**Frontend:**
1. FullCalendar integration
2. Google Calendar plugin setup
3. Task detail sidebar
4. Drag & drop functionality
5. Color coding
6. Filters

---

### Phase 3: Pomodoro Tracker (Priority 1)

**Backend:**
1. Pomodoro session management
2. Reflection processing
3. AI reflection analysis (Reflection Agent)
4. Streak system
5. Deep work score calculation

**Frontend:**
1. Timer UI
2. Task selection
3. Reflection form
4. Streak visualization
5. Progress bars

---

### Phase 4: AI Chat (Priority 2)

**Backend:**
1. Chat endpoints
2. Voice recording upload
3. OpenAI Whisper integration
4. Chat history with context
5. Supervisor Agent setup
6. LangGraph routing

**Frontend:**
1. Chat interface
2. Voice recording (Web Speech API / file upload)
3. Message history
4. Context-aware mode
5. Proactive suggestions

---

### Phase 5: Dashboard (Priority 2)

**Backend:**
1. Morning briefing generator (Insight Agent)
2. Daily summary aggregation
3. Streak data
4. Quick stats API

**Frontend:**
1. Dashboard layout
2. Current task card
3. Upcoming tasks
4. Streak display
5. Mini chart
6. Quick AI chat

---

### Phase 6: Reports & Analytics (Priority 3)

**Backend:**
1. Semantic search (Search Agent)
2. Embeddings generation
3. Vector search implementation
4. Report generation
5. Export functionality

**Frontend:**
1. Search interface
2. Time filters
3. Results display
4. Export buttons
5. Cross-references view

---

### Phase 7: Statistics (Priority 3)

**Backend:**
1. Statistics aggregation
2. Pattern detection (Insight Agent)
3. Productivity score calculation
4. Period comparison

**Frontend:**
1. Charts with Recharts
2. Stats cards
3. Insights display
4. Compare mode
5. Export for resume

---

### Phase 8: Advanced Features (Priority 4)

1. Weekly AI digest emails
2. Smart notifications (15 min before)
3. Energy tracking
4. Time boxing assistant
5. Batch similar tasks
6. Anti-procrastination mode
7. Auto-pause detector
8. Focus mode
9. PWA features

---

## 📝 Dependencies

### Backend (add to requirements.txt)
```txt
# Existing
fastapi
uvicorn
sqlalchemy[asyncio]
asyncpg
alembic
pydantic
pydantic-settings
python-jose[cryptography]
passlib[bcrypt]
python-multipart

# New - AI
langgraph
langchain
langchain-openai
anthropic
openai

# New - Supabase
supabase
storage3

# New - Google API
google-auth-oauthlib
google-api-python-client

# New - Other
python-dotenv
redis
celery
httpx
```

### Frontend (add to package.json)
```json
{
  "dependencies": {
    // Existing
    "next": "^15.0.0",
    "react": "^19.0.0",
    "typescript": "^5.0.0",
    "tailwindcss": "^3.4.0",
    "axios": "^1.6.0",

    // New - Calendar
    "@fullcalendar/react": "^6.1.0",
    "@fullcalendar/core": "^6.1.0",
    "@fullcalendar/daygrid": "^6.1.0",
    "@fullcalendar/timegrid": "^6.1.0",
    "@fullcalendar/list": "^6.1.0",
    "@fullcalendar/google-calendar": "^6.1.0",

    // New - State & UI
    "zustand": "^5.0.0",
    "recharts": "^2.12.0",
    "framer-motion": "^11.0.0",

    // New - Supabase
    "@supabase/supabase-js": "^2.45.0",
    "@supabase/auth-helpers-nextjs": "^0.10.0",

    // New - Voice
    "react-speech-kit": "^3.0.0",

    // New - Other
    "date-fns": "^3.0.0",
    "lucide-react": "^0.400.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.3.0"
  }
}
```

---

## 🔐 Environment Variables

### Backend (.env)
```env
# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

# AI
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback

# JWT
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database (если нужен прямой доступ)
DATABASE_URL=postgresql+asyncpg://...

# Redis
REDIS_URL=redis://localhost:6379
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

---

## 🎨 Design Principles

1. **Minimalism** - много белого пространства, фокус на контенте
2. **Dark mode** - опционально, но должен быть
3. **Smooth animations** - Framer Motion для переходов
4. **Responsive** - desktop-first, но mobile работает
5. **Accessibility** - ARIA labels, keyboard navigation
6. **Performance** - SSR/ISR где возможно, lazy loading

---

## 📋 Testing Strategy

1. **Backend** - Pytest + pytest-asyncio
2. **Frontend** - Jest + React Testing Library
3. **E2E** - Playwright
4. **AI Agents** - Unit tests для каждого агента

---

## 🚀 Deployment

### Frontend
- Vercel (zero-config Next.js)

### Backend
- Railway или Render (FastAPI + Docker)

### Database
- Supabase Cloud (managed)

### Storage
- Supabase Storage (voice recordings)

---

## 📖 Documentation Plan

1. **README.md** - обзор проекта
2. **CONTRIBUTING.md** - для контрибьюторов
3. **API.md** - API документация
4. **ARCHITECTURE.md** - архитектура
5. **AGENTS.md** - документация AI агентов
6. **DEPLOYMENT.md** - инструкции по деплою

---

## ✅ Success Criteria

Проект считается успешным, когда:

1. ✅ Пользователь может залогиниться через Google
2. ✅ Видит свой календарь с синхронизацией
3. ✅ Может начать Pomodoro сессию
4. ✅ После сессии проходит рефлексию
5. ✅ AI анализирует рефлексию и дает insights
6. ✅ Может общаться с AI голосом и текстом
7. ✅ Видит статистику и паттерны продуктивности
8. ✅ Может делать semantic search по истории
9. ✅ Получает AI рекомендации

---

**Последнее обновление:** 2026-01-11
**Статус документа:** Active - Использовать как primary source of truth для разработки
