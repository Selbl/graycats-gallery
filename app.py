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

    /* Added style for the cat count info */
    .cat-count-info {
        text-align: center;
        color: #8da9c4; 
        font-size: 1.1rem;
        margin-top: -15px; 
        margin-bottom: 25px;
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

    /* Slider styling for centered label */
    .stSlider > label {
        color: #ff85a2 !important;
        font-weight: bold !important;
        text-align: center;
        width: 100%;
        display: block;
        margin-bottom: 10px;
    }
    .stSlider > div > div > div[data-testid="stSlider"] {
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Logic to Fetch Images and Links ---
def get_cats(limit_per_subreddit=10):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) FloydAndFriedaBot/1.0"}
    subreddits = ["graycats", "dustkitties"]
    all_cats = []

    for sub in subreddits:
        count = 0
        # Fetch more posts from Reddit's API than needed to ensure we get 'limit_per_subreddit' *valid* images after filtering.
        url = f"https://www.reddit.com/r/{sub}/new.json?limit={limit_per_subreddit * 2}" 
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            
            for post in posts:
                if count >= limit_per_subreddit: break # Stop once desired number of images is reached
                
                p = post.get('data', {})
                img_url = ""
                post_link = f"https://www.reddit.com{p.get('permalink')}"

                url_dest = p.get('url_overridden_by_dest', '')
                if any(url_dest.lower().endswith(ext) for ext in ['.jpg', '.png', '.jpeg']):
                    img_url = url_dest
                
                elif p.get('is_gallery') and p.get('media_metadata'):
                    first_item_id = list(p['media_metadata'].keys())[0]
                    img_info = p['media_metadata'][first_item_id]['s']
                    if 'u' in img_info:
                        img_url = img_info['u']
                    elif 'mp4_url' in img_info:
                        img_url = img_info['mp4_url']

                elif p.get('preview') and p['preview'].get('images'):
                    img_url = p['preview']['images'][0]['source']['url']

                if img_url and "v.redd.it" not in img_url and not img_url.endswith(('.mp4', '.gifv')):
                    clean_url = img_url.replace("&amp;", "&")
                    all_cats.append({
                        "image": clean_url,
                        "post": post_link
                    })
                    count += 1
                    
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error for {sub}: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting for {sub}: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error for {sub}: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Other Request Error for {sub}: {err}")
        except Exception as e:
            print(f"An unexpected error occurred for {sub}: {e}")

    return all_cats

# --- User Interface ---

st.markdown("<h1>Floyd and Frieda's Dustkitty Gallery ✨</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>The world's premier collection of velvety gray fluff-clouds ฅ^•ﻌ•^ฅ</p>", unsafe_allow_html=True)

# Improvement: Add a slider for user to control the number of cats
desired_cats_per_subreddit = st.slider(
    "How many dustkitties per subreddit would you like to summon?",
    min_value=5, max_value=20, value=10, step=1,
    key="cat_slider"
)

if st.button("✨ SUMMON MORE CATS ✨"):
    # Clear the cache to ensure new content is fetched, even if the slider value hasn't changed
    st.cache_data.clear()
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

with st.spinner("Whispering to the dust kitties..."):
    # The cache key for cached_cats will now depend on the 'limit' argument
    @st.cache_data(ttl=600)
    def cached_cats(limit):
        return get_cats(limit)
    
    cat_list = cached_cats(desired_cats_per_subreddit) # Pass the slider value to the cached function

if cat_list:
    st.markdown(f"<p class='cat-count-info'>✨ Found {len(cat_list)} adorable dustkitties! Enjoy the fluff! 🐾</p>", unsafe_allow_html=True)
    
    cols = st.columns(2)
    for i, cat in enumerate(cat_list):
        with cols[i % 2]:
            st.markdown(f"### 🎀 Dustkitty {i+1}")
            
            st.markdown(f"""
                <div class="kitty-card">
                    <a href="{cat['post']}" target="_blank">
                        <img src="{cat['image']}" loading="lazy" alt="Dustkitty {i+1}">
                    </a>
                </div>
            """, unsafe_allow_html=True)
            st.write("") 
else:
    st.error("No cats found! Try clicking Summon again! 🐾")

st.markdown("<p style='text-align:center; color:#ff85a2; margin-top:50px;'>Stay Gray and Stay Fluffy! 🌫️</p>", unsafe_allow_html=True)