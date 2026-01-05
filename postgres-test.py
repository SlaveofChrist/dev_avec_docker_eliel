import psycopg2
import os
import redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins= ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

# Connexion
conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=5432,
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD"),
    database=os.getenv("POSTGRES_DB", "tp_note")
)
try: 
    r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True, socket_connect_timeout=2)
    r.ping() # On vérifie réellement la connexion
except (redis.Exceptions.ConnectionError, Exception):
    r = None # Dégradation : on continue sans cache

@app.get('/')
async def get_students():
    total_views = 0
    
    # --- ÉTAPE 1 : Tentative Redis (Dégradation élégante) ---
    if r is not None:
        try:
            total_views = r.incr('views:global_dashboard')
        except Exception:
            total_views = 0 
    
    # --- ÉTAPE 2 : Service Principal (Postgres) ---
    try:
        students_list = []
        cur = conn.cursor()
        cur.execute("SELECT nom, promo FROM students;")
        rows = cur.fetchall()
        
        for row in rows:
            students_list.append({
                "nom": row[0],
                "promo": row[1],
                "views": total_views 
            })
        cur.close()
        return students_list

    except Exception as e:
        return {"error": "Service momentanément indisponible", "details": str(e)}