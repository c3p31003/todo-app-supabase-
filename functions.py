import streamlit as st
import streamlit_authenticator as stauth

def get_users(supabase):
    res = supabase.table("users").select("*").execute()
    credentials = {"usernames": {}}
    for user in res.data:
        credentials["usernames"][user["username"]] = {
            "name": user["username"],   # ← "name"カラムの代わりにusernameを使う
            "password": user["password"]
        }
    return credentials

def register_user(supabase, username, password):
    hashed = stauth.Hasher.hash(password)
    supabase.table("users").insert({
        "username": username,
        "password": hashed
    }).execute()
    
def get_todos(supabase,user_id):
    """ DBからユーザーのタスク一覧を返す"""
    res = supabase.table("todos").select("id, task").eq("user_id", user_id).order("created_at").execute()
    rows = [(r["id"], r["task"]) for r in res.data]
    return rows

def add_todo(supabase,task, user_id):
    """ DBにタスクを追加する"""
    supabase.table("todos").insert({"task": task, "user_id": user_id}).execute()
    
    
def delete_todo(supabase,todo_id):
    """DBからタスクをtodo_idを元に削除する"""
    supabase.table("todos").delete().eq("id", todo_id).execute()
    

