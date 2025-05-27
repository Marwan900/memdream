import os
import base64
from io import BytesIO
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image



# Initialiser le client Nebius
client = OpenAI(
    base_url="https://api.studio.nebius.com/v1/",
    api_key=''
)

# Modèle de génération de texte
TEXT_MODEL = "meta-llama/Llama-3.3-70B-Instruct"

# Modèle de génération d'image
IMAGE_MODEL = "stability-ai/sdxl"

def generate_poetic_text(user_input: str) -> str:
    """Génère un texte poétique à partir de la description de l'utilisateur."""
    prompt = f"""
Tu es un poète onirique. Transforme cette description de rêve en un texte poétique et émotionnel :

"{user_input}"
"""
    response = client.chat.completions.create(
        model=TEXT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )
    return response.choices[0].message.content.strip()

def generate_image(prompt: str, output_path="outputs/dream_image.png") -> str:
    """Génère une image à partir d'un prompt."""
    # S'assurer que le prompt ne dépasse pas 2000 caractères
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

    # Décoder l'image et l'enregistrer
    b64_image = response.data[0].b64_json
    image_data = base64.b64decode(b64_image)
    image = Image.open(BytesIO(image_data))
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path)
    return output_path

def main():
    print("🌙 Bienvenue dans MemDream")
    user_input = input("Décrivez votre rêve ou souvenir marquant :\n> ")

    # Génération du texte poétique
    print("\n🧠 Génération du texte poétique...")
    poetic_text = generate_poetic_text(user_input)
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/dream_text.txt", "w", encoding="utf-8") as f:
        f.write(poetic_text)
    print("✅ Texte enregistré dans outputs/dream_text.txt")

    # Génération de l'image onirique
    print("\n🎨 Génération de l'image onirique...")
    image_prompt = poetic_text
    image_path = generate_image(image_prompt)
    print(f"✅ Image enregistrée à : {image_path}")

if __name__ == "__main__":
    main()
