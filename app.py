import streamlit as st
import requests

# --- Page Configuration ---
st.set_page_config(
    page_title="Floyd and Frieda's Dustkitty Gallery",
    page_icon="🐱",
    layout="wide"
)

# --- Custom Styling (Anime/Cute/Pastel Aesthetic) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;700&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Quicksand', sans-serif;
        background-color: #fff5f8;
    }

    .stApp {
        background-color: #fff5f8;
    }

    h1 {
        color: #ff85a2;
        text-align: center;
        font-size: 3.5rem !important;
        text-shadow: 3px 3px #ffe0e9;
        margin-bottom: 5px !important;
    }
            
    h3 {
        color: #ff85a2 !important;
        font-weight: 800 !important;
        text-shadow: 1px 1px #ffffff;
    }

    .subtitle {
        text-align: center;
        color: #8da9c4;
        font-size: 1.3rem;
        margin-bottom: 30px;
        font-weight: bold;
    }

    /* Image Styling applied to the HTML images */
    .kitty-card img {
        width: 100%;
        border-radius: 40px !important;
        border: 6px solid #ffffff !important;
        box-shadow: 8px 8px 0px #ffdae9;
        transition: transform 0.3s ease-in-out;
        cursor: pointer;
    }

    .kitty-card img:hover {
        transform: scale(1.02) rotate(1deg);
        border-color: #ffdae9 !important;
    }

    /* Summon Button Styling */
    div.stButton > button {
        background-color: #ff85a2 !important;
        background-image: none !important;
        color: white !important;
        border-radius: 50px !important;
        border: 3px solid #ffffff !important;
        padding: 15px 40px !important;
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: block;
        margin: 0 auto 30px auto !important;
        box-shadow: 0 8px 0px #d66d87 !important;
        transition: all 0.1s ease;
    }

    div.stButton > button * {
        background-color: transparent !important;
        color: white !important;
    }

    div.stButton > button:hover {
        background-color: #ff7091 !important;
        border-color: #ffffff !important;
    }

    div.stButton > button:active {
        transform: translateY(4px);
        box-shadow: 0 4px 0px #d66d87 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Logic to Fetch Images and Links ---
def get_cats():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) FloydAndFriedaBot/1.0"}
    subreddits = ["graycats", "dustkitties"]
    all_cats = []

    for sub in subreddits:
        count = 0
        url = f"https://www.reddit.com/r/{sub}/new.json?limit=40"
        
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            
            for post in posts:
                if count >= 10: break
                
                p = post.get('data', {})
                img_url = ""
                # Get the reddit post link
                post_link = f"https://www.reddit.com{p.get('permalink')}"

                # 1. Standard Image
                url_dest = p.get('url_overridden_by_dest', '')
                if any(url_dest.lower().endswith(ext) for ext in ['.jpg', '.png', '.jpeg']):
                    img_url = url_dest
                
                # 2. Gallery Support
                elif p.get('is_gallery') and p.get('media_metadata'):
                    first_item_id = list(p['media_metadata'].keys())[0]
                    img_url = p['media_metadata'][first_item_id]['s']['u']

                # 3. Preview Fallback
                elif p.get('preview'):
                    img_url = p['preview']['images'][0]['source']['url']

                if img_url and "v.redd.it" not in img_url:
                    clean_url = img_url.replace("&amp;", "&")
                    # Store both image and post link
                    all_cats.append({
                        "image": clean_url,
                        "post": post_link
                    })
                    count += 1
                    
        except Exception:
            pass 

    return all_cats

# --- User Interface ---

st.markdown("<h1>Floyd and Frieda's Dustkitty Gallery ✨</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>The world's premier collection of velvety gray fluff-clouds ฅ^•ﻌ•^ฅ</p>", unsafe_allow_html=True)

if st.button("✨ SUMMON MORE CATS ✨"):
    st.cache_data.clear()
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

with st.spinner("Whispering to the dust kitties..."):
    @st.cache_data(ttl=600)
    def cached_cats():
        return get_cats()
    cat_list = cached_cats()

if cat_list:
    cols = st.columns(2)
    for i, cat in enumerate(cat_list):
        with cols[i % 2]:
            st.markdown(f"### 🎀 Dustkitty {i+1}")
            
            # Use raw HTML to wrap the image in a link
            # 'target="_blank"' makes it open in a new tab
            st.markdown(f"""
                <div class="kitty-card">
                    <a href="{cat['post']}" target="_blank">
                        <img src="{cat['image']}">
                    </a>
                </div>
            """, unsafe_allow_html=True)
            st.write("") 
else:
    st.error("No cats found! Try clicking Summon again! 🐾")

st.markdown("<p style='text-align:center; color:#ff85a2; margin-top:50px;'>Stay Gray and Stay Fluffy! 🌫️</p>", unsafe_allow_html=True)