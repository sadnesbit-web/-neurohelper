import sqlite3
from datetime import date
DB_NAME='neurohelper.db'
def get_connection(): return sqlite3.connect(DB_NAME)
def init_db():
 c=get_connection(); c.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT, requests_today INTEGER DEFAULT 0, last_request_date TEXT, is_pro INTEGER DEFAULT 0, created_at TEXT DEFAULT CURRENT_TIMESTAMP)'''); c.commit(); c.close()
def add_user(user_id,username,first_name):
 c=get_connection(); c.execute('INSERT OR IGNORE INTO users (user_id,username,first_name) VALUES (?,?,?)',(user_id,username,first_name)); c.execute('UPDATE users SET username=?, first_name=? WHERE user_id=?',(username,first_name,user_id)); c.commit(); c.close()
def get_user(user_id):
 c=get_connection(); r=c.execute('SELECT user_id,username,first_name,requests_today,last_request_date,is_pro FROM users WHERE user_id=?',(user_id,)).fetchone(); c.close(); return r
def get_usage(user_id):
 u=get_user(user_id)
 if not u: return 0,False
 return (0,bool(u[5])) if u[4]!=str(date.today()) else (u[3] or 0,bool(u[5]))
def increment_usage(user_id):
 today=str(date.today()); c=get_connection(); c.execute('UPDATE users SET requests_today=CASE WHEN last_request_date=? THEN requests_today+1 ELSE 1 END,last_request_date=? WHERE user_id=?',(today,today,user_id)); c.commit(); c.close()
def get_stats():
 c=get_connection(); a=c.execute('SELECT COUNT(*) FROM users').fetchone()[0]; b=c.execute('SELECT COUNT(*) FROM users WHERE is_pro=1').fetchone()[0]; c.close(); return a,b
