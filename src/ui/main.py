from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import gradio as gr
from app import iface

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint for Render
@app.get("/")
def read_root():
    return {"message": "Gradio UI is running."}

# Mount Gradio at /gradio
app = gr.mount_gradio_app(app, iface, path="/gradio")
