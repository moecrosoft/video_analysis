import os
import uuid
import psycopg2
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model import extract_captions, summarise_with_ollama

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

def get_db():
    return psycopg2.connect(
        dbname = os.getenv('POSTGRES_DB'),
        user = os.getenv('POSTGRES_USER'),
        password = os.getenv('POSTGRES_PASSWORD'),
        host = os.getenv('POSTGRES_HOST')
    )

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(''' 
        CREATE TABLE IF NOT EXISTS summaries (
                id SERIAL PRIMARY KEY,
                filename TEXT,
                summary TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
    ''')
    conn.commit()
    cur.close()
    conn.close()

init_db()

@app.post('/analyse')
async def analyse(file: UploadFile = File(...)):
    tmp_path = f'/tmp/{uuid.uuid4()}.mp4'
    try:
        with open(tmp_path, 'wb') as f:
            f.write(await file.read())

        captions = extract_captions(tmp_path)
        if not captions:
            raise HTTPException(status_code=400, detail='No frames extracted from video')
        
        summary = summarise_with_ollama(captions)

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO summaries (filename, summary) VALUES (%s, %s)',
            (file.filename, summary)
        )
        conn.commit()
        cur.close()
        conn.close()

        return {'summary': summary, 'frames_analysed': len(captions)}
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

@app.get('/history')
def history():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT filename, summary, created_at FROM summaries ORDER BY created_at DESC')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{'filename': r[0], 'summary': r[1], 'created_at': str(r[2])} for r in rows]