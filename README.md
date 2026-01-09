# Avatar Sync – Quickstart

This repository provides a **quickstart pipeline** for generating a **talking avatar video** by syncing an input **audio file** with a **static face image** using deep learning–based lip synchronization.

The `quickstart.py` script is designed to help you run the full pipeline with minimal setup.

---

##  What does `quickstart.py` do?

- Takes an **input face image**
- Takes an **input audio file**
- Uses a lip-sync model (Wav2Lip-based workflow)
- Generates a **synchronized talking avatar video**

---

##  Project Structure (Relevant)

avatar_sync/
- quickstart.py # Entry point (this file)
- wav2lip_workspace/ # Model & inference workspace
- requirements.txt # Python dependencies
- .gitignore
