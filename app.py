import streamlit as st
import requests
import random

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

    /* --- NEW: Kitty Card Container with Skeleton Loader Effect --- */
    .kitty-card-container {
        position: relative;
        width: 100%;
        min-height: 250px; /* Ensure placeholder height for skeleton */
        border-radius: 40px !important;
        border: 6px solid #ffffff !important;
        box-shadow: 8px 8px 0px #ffdae9;
        background-color: #f0f0f0; /* Skeleton background color */
        overflow: hidden; /* For shimmer effect */
        display: flex; /* To center loading text */
        align-items: center; /* To center loading text */
        justify-content: center; /* To center loading text */
        color: #bbb; /* Color for loading text */
        font-size: 0.9rem;
        font-style: italic;
        margin-bottom: 0px; /* Space between cards, adjusted for new post details */
    }

    /* Shimmer animation for the skeleton loader */
    .kitty-card-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: -150%; /* Start off-screen */
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shimmer 1.5s infinite;
        z-index: 1; /* Above background, below image */
    }

    @keyframes shimmer {
        0% { left: -150%; }
        100% { left: 150%; }
    }

    /* Image Styling applied to the HTML images within the container */
    .kitty-card-container img {
        width: 100%;
        height: auto; /* Maintain aspect ratio */
        border-radius: 40px !important; /* Apply border-radius to image */
        border: 6px solid #ffffff !important; /* Apply border to image */
        box-shadow: 8px 8px 0px #ffdae9; /* Apply shadow to image */
        transition: transform 0.3s ease-in-out;
        cursor: pointer;
        display: block; /* Ensure it covers the parent */
        position: relative; /* To be on top of skeleton and shimmer */
        z-index: 2; /* Ensure image is above shimmer */
    }

    .kitty-card-container img:hover {
        transform: scale(1.02) rotate(1deg);
        border-color: #ffdae9 !important;
    }
    /* --- END NEW --- */

    /* NEW: Styling for the post title and subreddit details */
    .kitty-post-details {
        text-align: center;
        color: #8da9c4;
        font-size: 0.95rem;
        margin-top: 10px; /* Space above title */
        margin-bottom: 20px; /* Space below details, between cards */
        line-height: 1.3;
    }
    .kitty-post-details .subreddit {
        font-style: italic;
        font-size: 0.85rem;
        color: #b0c4de; /* A slightly lighter shade */
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
    error_messages = [] # List to store user-facing error messages

    for sub in subreddits:
        count = 0
        # Fetch more posts from Reddit's API than needed to ensure we get 'limit_per_subreddit' *valid* images after filtering.
        url = f"https://www.reddit.com/r/{sub}/new.json?limit={limit_per_subreddit * 2}" 
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
            data = response.json().get('data', {}).get('children', []) # Directly get children here
            
            for post in data: # Iterate over data directly
                if count >= limit_per_subreddit: break # Stop once desired number of images is reached
                
                p = post.get('data', {})
                img_url = ""
                post_link = f"https://www.reddit.com{p.get('permalink')}"

                url_dest = p.get('url_overridden_by_dest', '')
                if any(url_dest.lower().endswith(ext) for ext in ['.jpg', '.png', '.jpeg']):
                    img_url = url_dest
                
                elif p.get('is_gallery') and p.get('media_metadata'):
                    # Handle galleries by taking the first image
                    first_item_id = list(p['media_metadata'].keys())[0]
                    img_info = p['media_metadata'][first_item_id]['s']
                    if 'u' in img_info: # Original image URL
                        img_url = img_info['u']
                    elif 'mp4_url' in img_info: # Fallback for videos in galleries (though we filter videos later)
                        img_url = img_info['mp4_url']

                elif p.get('preview') and p['preview'].get('images'):
                    img_url = p['preview']['images'][0]['source']['url']

                if img_url and "v.redd.it" not in img_url and not img_url.endswith(('.mp4', '.gifv')):
                    clean_url = img_url.replace("&amp;", "&")
                    all_cats.append({
                        "image": clean_url,
                        "post": post_link,
                        "title": p.get('title', 'Untitled Cat Post'),
                        "subreddit": p.get('subreddit', 'Unknown Subreddit')
                    })
                    count += 1
                    
        except requests.exceptions.HTTPError as errh:
            error_messages.append(f"HTTP Error fetching from r/{sub}: {errh}")
        except requests.exceptions.ConnectionError as errc:
            error_messages.append(f"Network Connection Error fetching from r/{sub}: {errc}")
        except requests.exceptions.Timeout as errt:
            error_messages.append(f"Timeout Error fetching from r/{sub}: {errt}")
        except requests.exceptions.RequestException as err:
            error_messages.append(f"An unknown request error occurred for r/{sub}: {err}")
        except Exception as e:
            error_messages.append(f"An unexpected error occurred while processing r/{sub}: {e}")

    return all_cats, error_messages

# --- User Interface ---

st.markdown("<h1>Floyd and Frieda's Dustkitty Gallery ✨</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>The world's premier collection of velvety gray fluff-clouds ฅ^•ﻌ•^ฅ</p>", unsafe_allow_html=True)

# NEW: Function to update query parameters on slider change
def update_slider_query_params():
    st.query_params["cats_per_sub"] = str(st.session_state.cat_slider)
    st.query_params["columns"] = str(st.session_state.column_slider)

# NEW: Get initial values from query parameters or set defaults
# Use .get() method with a default value to avoid KeyError if param is not present
initial_cats_per_sub = int(st.query_params.get("cats_per_sub", 10))
initial_columns = int(st.query_params.get("columns", 2))

desired_cats_per_subreddit = st.slider(
    "How many dustkitties per subreddit would you like to summon?",
    min_value=5, max_value=20, value=initial_cats_per_sub, step=1,
    key="cat_slider",
    on_change=update_slider_query_params # Call function when slider changes
)

num_columns = st.slider(
    "How many columns would you like in your gallery?",
    min_value=1, max_value=4, value=initial_columns, step=1,
    key="column_slider",
    on_change=update_slider_query_params # Call function when slider changes
)

if st.button("✨ SUMMON MORE CATS ✨"):
    st.cache_data.clear()
    st.rerun() # Use st.rerun directly

with st.spinner("Whispering to the dust kitties..."):
    @st.cache_data(ttl=600)
    def cached_cats(limit):
        return get_cats(limit)
    
    # Pass the current value from the slider, which might have been initialized from query_params
    cat_list, errors = cached_cats(desired_cats_per_subreddit) 
    random.shuffle(cat_list)

# Display error messages to the user if any occurred during fetching
if errors:
    st.markdown("<p class='cat-count-info' style='color:#ff6347; margin-bottom: 10px;'>🐾 Encountered some issues:</p>", unsafe_allow_html=True)
    for error_msg in errors:
        st.warning(error_msg)

if cat_list:
    st.markdown(f"<p class='cat-count-info'>✨ Found {len(cat_list)} adorable dustkitties! Enjoy the fluff! 🐾</p>", unsafe_allow_html=True)
    
    cols = st.columns(num_columns)
    for i, cat in enumerate(cat_list):
        with cols[i % num_columns]:
            # Using explicit h3 tag for consistent styling application
            st.markdown(f"<h3>🎀 Dustkitty {i+1}</h3>", unsafe_allow_html=True) 
            
            st.markdown(f"""
                <div class="kitty-card-container">
                    Summoning fluff...
                    <a href="{cat['post']}" target="_blank">
                        <img src="{cat['image']}" loading="lazy" alt="Dustkitty {i+1}">
                    </a>
                </div>
                <div class="kitty-post-details">
                    <strong>{cat['title']}</strong><br>
                    <span class="subreddit">from r/{cat['subreddit']}</span>
                </div>
            """, unsafe_allow_html=True)
else:
    # Only show this generic "No cats found" message if there were no specific API errors reported
    if not errors: 
        st.error("No cats found! Try clicking Summon again! 🐾")

st.markdown("<p style='text-align:center; color:#ff85a2; margin-top:50px;'>Stay Gray and Stay Fluffy! 🌫️</p>", unsafe_allow_html=True)