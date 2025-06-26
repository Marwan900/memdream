# MemDream

**L’IA qui peint vos rêves.**  
Par **Marwan** et **Erwan**

---

## 🎯 Description

**MemDream** est une application qui transforme vos **rêves ou souvenirs** en véritables **aventures poétiques et visuelles**. Grâce à l’intelligence artificielle, une simple description devient un **texte onirique**, accompagné d’**illustrations générées automatiquement** et d’une **narration audio immersive**.

---

## 🧠 Fonctionnalités

- 📝 Input utilisateur : **description libre d’un rêve**
- 🧾 Génération de **texte poétique** (modèle LLM - LLaMA 3 via Nebius)
- 🎨 Création d’**images surréalistes** via un modèle de diffusion (SDXL)
- 🔊 Synthèse vocale **automatique en français** (gTTS)
- 📖 Présentation finale sous forme de **livre animé** (texte, image, audio)

---

## ⚙️ Technologies utilisées

- **Python**
- **Streamlit** – interface interactive
- **OpenAI API (Nebius)** – génération de texte et d’images
- **gTTS** – synthèse vocale en français
- **PIL (Pillow)** – manipulation et affichage d’images

---

## 🚀 Lancer l’application

1. **Cloner le dépôt** :  
   ```bash
   git clone https://github.com/votre-utilisateur/memdream.git
   cd memdream
    ```
   
2. **Installer les dépendances** : 
  ```bash
pip install -r requirements.txt
  ```

3. **Définir votre clé API (Nebius)** :
  ```bash
export NEBIUS_API_KEY="votre_clé_API"
  ```

4. **Définir votre clé API (Nebius)** 
  ```bash
streamlit run app.py
  ```

