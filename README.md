# Todo App (Streamlit + Supabase)

Supabase をバックエンドに使ったシンプルな Todo アプリです。  
`streamlit-authenticator` を使ってユーザー登録・ログインを行い、ユーザーごとに Todo を管理します。

## 必要環境

- Python 3.11+
- Supabase プロジェクト

## セットアップ

1. 依存関係をインストール

```bash
pip install -r requirements.txt
```

2. Streamlit secrets を作成（`.streamlit/secrets.toml`）

```toml
SUPABASE_URL = "https://<your-project>.supabase.co"
SUPABASE_KEY = "<your-anon-or-service-role-key>"

[cookie]
name = "todo_app_cookie"
key = "replace-with-random-secret"
expiry_days = 30
```

3. Supabase 側でテーブルを用意

- `users` テーブル: `username`, `password`
- `todos` テーブル: `id`, `task`, `user_id`, `created_at`

## 起動

```bash
streamlit run web.py
```

## 主要ファイル

- `web.py`: Streamlit UI と認証・画面制御
- `functions.py`: Supabase への CRUD 処理

