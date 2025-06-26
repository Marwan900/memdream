import os
import base64
from io import BytesIO
from datetime import datetime

import streamlit as st
from PIL import Image
from gtts import gTTS
from openai import OpenAI
import time
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

# Configuration Streamlit
st.set_page_config(page_title="MemDream", layout="wide")

# API Key Nebius
API_KEY = os.getenv("NEBIUS_API_KEY") or "YOUR_API_KEY"

# Initialisation du client Nebius
client = OpenAI(
    base_url="https://api.studio.nebius.com/v1/",
    api_key='eyJhbGciOiJIUzI1NiIsImtpZCI6IlV6SXJWd1h0dnprLVRvdzlLZWstc0M1akptWXBvX1VaVkxUZlpnMDRlOFUiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiJnb29nbGUtb2F1dGgyfDEwNDgwNDEyODkyNjY3NDgxODExMyIsInNjb3BlIjoib3BlbmlkIG9mZmxpbmVfYWNjZXNzIiwiaXNzIjoiYXBpX2tleV9pc3N1ZXIiLCJhdWQiOlsiaHR0cHM6Ly9uZWJpdXMtaW5mZXJlbmNlLmV1LmF1dGgwLmNvbS9hcGkvdjIvIl0sImV4cCI6MTkwNjAyNzMyOCwidXVpZCI6IjMzOWZkOTg4LWFiOGEtNGVmYy04MzM1LTU4ZWU1YmU4NDFiNyIsIm5hbWUiOiJtZW1kcmVhbSIsImV4cGlyZXNfYXQiOiIyMDMwLTA1LTI2VDEyOjAyOjA4KzAwMDAifQ.Nfx0eFBtSe62YrIuxiPlJxJxcV9rALBZmhIw_bxI_MA'
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
    sentences = [s.strip() for s in text.split(". ") if s.strip()]
    scenes = []
    current = ""
    for sentence in sentences:
        if len(current) + len(sentence) < max_len:
            current += sentence + ". "
        else:
            scenes.append(current.strip())
            current = sentence + ". "
    if current.strip():
        scenes.append(current.strip())
    return scenes

def generate_image(prompt: str) -> Image.Image:
    prompt = prompt.strip()
    if not prompt:
        raise ValueError("Prompt vide transmis à l'IA.")

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

def create_video(scenes, images, audio_paths, output_path="outputs/memdream_video.mp4"):
    clips = []
    for i, (scene, image, audio) in enumerate(zip(scenes, images, audio_paths)):
        img_path = f"outputs/temp_scene_{i}.png"
        image.save(img_path)

        audio_clip = AudioFileClip(audio)
        img_clip = ImageClip(img_path).with_duration(audio_clip.duration)
        
        # Transformer image en vidéo puis ajouter audio via CompositeVideoClip
        clip = img_clip.with_audio(audio_clip)
        clips.append(clip)

    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(output_path, fps=24)
    return output_path



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
st.write("Décrivez un rêve ou un souvenir marquant. Laissez l'IA le transformer en une aventure visuelle, sonore et animée ✨")

user_input = st.text_area("Votre rêve", height=150)
generate = st.button("Générer mon rêve")

if generate and user_input:
    with st.spinner("🧠 Génération du texte poétique..."):
        poetic_text = generate_poetic_text(user_input)

    scenes = split_text_into_scenes(poetic_text)
    filtered_scenes = [s for s in scenes if s.strip()]

    with st.spinner("🎨 Création des images de couverture et de scènes..."):
        cover_img = generate_image("Illustration de couverture du rêve : " + user_input)
        st.image(cover_img, caption="🌌 Couverture du rêve", use_column_width=True)

        images = []
        for i, scene in enumerate(filtered_scenes):
            try:
                img = generate_image(scene)
                images.append(img)
            except Exception as e:
                st.error(f"Erreur lors de la génération d'image pour une scène : {e}")

    with st.spinner("🔊 Création de la narration audio..."):
        audio_dir = "outputs"
        os.makedirs(audio_dir, exist_ok=True)
        audio_files = []
        for i, scene in enumerate(filtered_scenes):
            path = f"{audio_dir}/scene_{i+1}.mp3"
            save_audio(scene, path)
            audio_files.append(path)

    with st.spinner("🎥 Création de la vidéo onirique..."):
        video_path = create_video(filtered_scenes, images, audio_files)

    st.header("📽️ Vidéo de votre rêve")
    with open(video_path, "rb") as f:
        video_bytes = f.read()
        st.video(video_bytes)

elif generate and not user_input:
    st.warning("Veuillez décrire un rêve avant de générer.")
