# 🐾 Floyd and Frieda's Dustkitty Gallery ✨

Welcome to the world's premier collection of velvety gray fluff-clouds! ฅ^•ﻌ•^ฅ

This is a lightweight, single-page web application built with Streamlit. It automatically fetches, filters, and displays the newest photos of gray cats directly from Reddit's `r/graycats` and `r/dustkitties` communities, wrapped up in a custom pastel, anime-inspired aesthetic.

## 🚀 The Origin Story
This entire application was **vibe coded in just a couple of minutes using Google AI Studio and Gemini**. It serves as a rapid-prototyping experiment to test AI-assisted development, prompt engineering for UI/UX constraints, and API data wrangling—all contained within a single Python script.

I also love gray cats, and my fluffy friends Floyd and Frieda wanted to see more cats that look like them. Which is why I made this!

## ✨ Features
* **Live Fluff Fetching:** Pulls the 10 newest valid image posts from both `r/graycats` and `r/dustkitties`.
* **Smart Filtering:** Bypasses text posts, handles Reddit gallery metadata, and ignores video links to ensure a clean visual grid.
* **Custom Aesthetic:** Features a fully custom CSS injection for a soft pastel color palette, rounded "sticker" image borders, hover animations, and a highly styled "Summon" button.
* **One-Click Refresh:** A prominent button clears the Streamlit cache and fetches a fresh batch of cats instantly.

## 📂 Repository Structure
Keeping it simple and clean:
* `app.py`: The complete Streamlit application (frontend UI and backend API logic).
* `README.md`: You are reading it!

## 🛠️ How to Run Locally

You only need Python and two libraries to run this on your machine. 

**1. Install the required dependencies:**
Open your terminal and run:
```bash
pip install streamlit requests

```

**2. Summon the cats:**
Navigate to the repository folder in your terminal and run:

```bash
streamlit run app.py

```

**3. View the gallery:**
Your browser should automatically open a new tab pointing to `http://localhost:8501`.

---

*Stay Gray and Stay Fluffy! 🌫️*