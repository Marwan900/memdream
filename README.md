# MemDream

**Par Marwan [Nom] et Erwan [Nom]**

---

## 1. Description du projet

MemDream est une application qui transforme vos rêves ou souvenirs en aventures poétiques et visuelles. Grâce à l’intelligence artificielle, une simple description textuelle est convertie en un texte onirique, accompagné d’illustrations générées automatiquement et d’une narration audio immersive.

---

## 2. Cas d’usage

- Un utilisateur souhaite immortaliser un rêve ou un souvenir marquant.
- Il saisit une description libre de son rêve dans l’interface.
- L’application génère un récit poétique, des images surréalistes et une narration audio.
- L’utilisateur peut visualiser son rêve sous forme d’un livre animé (texte, images, audio).

---

## 3. Fonctionnalités principales

- Description libre d’un rêve ou souvenir par l’utilisateur.
- Génération automatique de texte poétique avec un modèle LLM (LLaMA 3 via Nebius).
- Création d’images surréalistes par un modèle de diffusion (SDXL).
- Synthèse vocale en français avec gTTS pour narration immersive.
- Interface web interactive avec Streamlit affichant le récit, les images et l’audio.

---

## 4. Outils IA utilisés

- **LLaMA 3 (Nebius API)** pour la génération du texte poétique.
- **Modèle SDXL (Nebius API)** pour la création d’images.
- **gTTS** pour la synthèse vocale en français.

---

## 5. Limitations identifiées

- La génération des images peut être lente selon la charge du serveur Nebius.
- La qualité du texte dépend de la description initiale fournie par l’utilisateur.
- La synthèse vocale utilise gTTS, limitée aux voix disponibles via Google Text-to-Speech.
- Le projet nécessite une clé API Nebius valide et active.

---

## 6. Captures d’écran / Démo

![Exemple de résultat](lien_vers_capture.png)  
*Capture d’écran de l’interface MemDream affichant un rêve généré*

---

## 7. Instructions pour tester ou comprendre le projet

### Installation
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

