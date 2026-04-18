from urllib import response

import gradio as gr

def respond(message, history):
    response = f"You said {message}\
        \nAnd I say I love learning AI Enginerring"
    return response

gr.ChatInterface(fn=respond).launch()