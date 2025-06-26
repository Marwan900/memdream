
import os
import base64
from io import BytesIO
from datetime import datetime

import streamlit as st
from PIL import Image
from gtts import gTTS
from openai import OpenAI
import time

# Configuration Streamlit
st.set_page_config(page_title="MemDream", layout="wide")

# API Key Nebius
API_KEY = os.getenv("NEBIUS_API_KEY") or "YOUR_API_KEY"

# Initialisation du client Nebius
client = OpenAI(
    base_url="https://api.studio.nebius.com/v1/",
    api_key=''
)

# Modèles IA
TEXT_MODEL = "meta-llama/Llama-3.3-70B-Instruct"
IMAGE_MODEL = "stability-ai/sdxl"

def generate_poetic_text(description: str) -> str:
    prompt = f"""
Transforme cette description de rêve en un texte poétique, émotionnel et coloré :
"{description}"
"""
    response = client.chat.completions.create(
        model=TEXT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )
    return response.choices[0].message.content.strip()

def split_text_into_scenes(text: str, max_len=400) -> list:
    sentences = text.split(". ")
    scenes = []
    current = ""
    for sentence in sentences:
        if len(current) + len(sentence) < max_len:
            current += sentence + ". "
        else:
            scenes.append(current.strip())
            current = sentence + ". "
    if current:
        scenes.append(current.strip())
    return scenes

def generate_image(prompt: str) -> Image.Image:
    if len(prompt) > 2000:
        prompt = prompt[:2000]

    response = client.images.generate(
        model=IMAGE_MODEL,
        prompt=prompt,
        response_format="b64_json",
        extra_body={
            "response_extension": "png",
            "width": 1024,
            "height": 1024,
            "num_inference_steps": 30,
            "negative_prompt": "",
            "seed": -1
        }
    )

    b64_image = response.data[0].b64_json
    image_data = base64.b64decode(b64_image)
    image = Image.open(BytesIO(image_data))
    return image

def save_audio(text: str, path: str):
    tts = gTTS(text=text, lang='fr')
    tts.save(path)

# 🎨 Interface onirique
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #1c1c3c, #292954);
        color: #e0e0f0;
        font-family: 'Georgia', serif;
    }
    .title-text {
        text-shadow: 0 0 10px #8a2be2;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌙 MemDream - Peignez vos rêves")
st.write("Décrivez un rêve ou un souvenir marquant. Laissez l'IA le transformer en une aventure visuelle et sonore ✨")

user_input = st.text_area("Votre rêve", height=150)
generate = st.button("Générer mon rêve")

if generate and user_input:
    with st.spinner("🧠 Génération du texte poétique..."):
        poetic_text = generate_poetic_text(user_input)

    scenes = split_text_into_scenes(poetic_text)

    st.subheader("📖 Récit onirique")
    st.markdown(f"<div style='background-color:#2e2e48;padding:15px;border-radius:10px;'>{poetic_text}</div>", unsafe_allow_html=True)

    with st.spinner("🎨 Création des scènes visuelles..."):
        images = []
        for i, scene in enumerate(scenes):
            img = generate_image(scene)
            images.append((scene, img))

    with st.spinner("🔊 Création de la narration..."):
        audio_dir = "outputs"
        os.makedirs(audio_dir, exist_ok=True)
        audio_files = []
        for i, (scene, _) in enumerate(images):
            path = f"{audio_dir}/scene_{i+1}.mp3"
            save_audio(scene, path)
            audio_files.append(path)

    st.header("📘 Livre onirique animé")
    for i, (scene, img) in enumerate(images):
        with st.container():
            st.image(img, caption=f"Scène {i+1}", use_column_width=True)
            st.markdown(f"<div style='background-color:#2e2e48;padding:10px;border-radius:10px;'>{scene}</div>", unsafe_allow_html=True)
            st.audio(audio_files[i])
            time.sleep(1)

elif generate and not user_input:
    st.warning("Veuillez décrire un rêve avant de générer.")
