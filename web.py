import streamlit as st
import functions
import streamlit_authenticator as stauth
import os
from dotenv import load_dotenv
from supabase import create_client
import inspect
print(inspect.getfile(functions))
print(inspect.signature(functions.register_user))
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

# DBからユーザー一覧を取得
credentials = functions.get_users(supabase)

cookie = st.secrets["cookie"]

authenticator = stauth.Authenticate(
    credentials,
    cookie["name"],
    cookie["key"],
    cookie["expiry_days"]
)

# ログイン処理は1回だけ
authenticator.login(location="main")

# ログイン結果を取得
auth_status = st.session_state.get("authentication_status")
username = st.session_state.get("username")

if auth_status:
    # ログイン済み：Todoアプリ
    authenticator.logout("Logout", "sidebar")
    st.title(f"My Todo App - {username}")

    def add_todo():
        task = st.session_state["new_todo"].strip()
        if task:
            functions.add_todo(supabase, task, username)
        st.session_state["new_todo"] = ""

    todos = functions.get_todos(supabase, username)

    for todo_id, task in todos:
        if st.checkbox(task, key=todo_id):
            functions.delete_todo(supabase, todo_id)
            st.rerun()

    st.text_input(
        label="Add new todo",
        placeholder="Add new todo...",
        on_change=add_todo,
        key="new_todo"
    )

elif auth_status is False:
    # ログイン失敗
    st.error("ユーザ名かパスワードが違うみたい🤔")

    st.divider()
    st.subheader("新規登録")
    with st.form("register_form"):
        new_username = st.text_input("ユーザー名")
        new_password = st.text_input("パスワード", type="password")
        submitted = st.form_submit_button("登録")
        if submitted:
            if new_username and new_password:
                functions.register_user(supabase, new_username,new_password)
                st.success("登録完了🥳！ログインして👀")
            else:
                st.warning("ぜんぶうめて！！！！！😠")

else:
    # 未ログイン
    st.warning("まずはログインしてね🤨")

    st.divider()
    st.subheader("新規登録")
    with st.form("register_form"):
        new_username = st.text_input("ユーザー名")
        new_password = st.text_input("パスワード", type="password")
        submitted = st.form_submit_button("登録")
        if submitted:
            if new_username and new_password:
                functions.register_user(supabase, new_username, new_password)
                st.success("登録完了🥳！ログインして👀")
            else:
                st.warning("ぜんぶうめて！！！！！😠")