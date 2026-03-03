# Django + React (Next.js) プロジェクト構成

## ディレクトリ構成

```
src/kadai/
├── backend/                    # Django プロジェクト
│   ├── manage.py
│   ├── config/                 # Django プロジェクト設定
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── api/                    # Django アプリケーション
│       ├── __init__.py
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       └── migrations/
└── frontend/                   # Next.js プロジェクト
    ├── package.json
    ├── tsconfig.json
    ├── next.config.js
    └── src/
        ├── app/                # App Router
        │   ├── layout.tsx
        │   └── page.tsx
        ├── components/         # React コンポーネント
        └── lib/                # ユーティリティ・API クライアント
```

## 技術スタック

### バックエンド
- Python 3.12+
- Django 4.2+
- Django REST Framework 3.14+
- pytest + pytest-django

### フロントエンド
- Node.js 20+
- Next.js 14+ (App Router)
- React 18+
- TypeScript 5+
- Jest + React Testing Library

### 開発環境
- Docker Compose（バックエンド + フロントエンド + DB）
- VSCode Dev Containers

## Docker Compose 構成（参考）

```yaml
services:
  backend:
    build: ./src/kadai/backend
    ports:
      - "8000:8000"
    volumes:
      - ./src/kadai/backend:/app
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings

  frontend:
    build: ./src/kadai/frontend
    ports:
      - "3000:3000"
    volumes:
      - ./src/kadai/frontend:/app
    depends_on:
      - backend

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: kadai
      POSTGRES_USER: kadai
      POSTGRES_PASSWORD: kadai
```

## テスト実行

### バックエンド
```bash
# 全バックエンドテスト
pytest tests/stages/ -v

# ステージ別
pytest -m stage01 -v
```

### フロントエンド
```bash
# 全フロントエンドテスト
npx jest tests/stages/ --passWithNoTests

# ステージ別
npx jest tests/stages/stage01/ --passWithNoTests
```

### CI（GitHub Classroom）
各ステージで backend → frontend の順にテストを実行し、両方が通過した場合にステージクリアとする。
