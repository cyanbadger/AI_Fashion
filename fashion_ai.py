
import requests, os
from PIL import Image
from io import BytesIO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import urllib.parse

PRODUCT_CATALOGUE = [
    {"name": "Floral Midi Dress",  "price": "₹799",   "brand": "FabIndia",    "url": "https://www.myntra.com", "tags": "floral summer dress flowy"},
    {"name": "Printed Wrap Dress", "price": "₹1,199", "brand": "W for Woman", "url": "https://www.myntra.com", "tags": "printed wrap casual dress"},
    {"name": "Boho Sundress",      "price": "₹649",   "brand": "Aurelia",     "url": "https://www.myntra.com", "tags": "boho floral summer light"},
    {"name": "Denim Jacket",       "price": "₹999",   "brand": "Roadster",    "url": "https://www.myntra.com", "tags": "denim jacket casual streetwear"},
    {"name": "Embroidered Kurti",  "price": "₹549",   "brand": "Biba",        "url": "https://www.myntra.com", "tags": "embroidered ethnic cotton kurti"},
    {"name": "Palazzo Pants",      "price": "₹699",   "brand": "Global Desi", "url": "https://www.myntra.com", "tags": "palazzo wide leg pants ethnic"},
    {"name": "Crop Top",           "price": "₹399",   "brand": "H&M",         "url": "https://www.myntra.com", "tags": "crop top casual western summer"},
]

def enhance_prompt(prompt):
    return (
        "fashion design, clothing sketch, high quality, detailed, "
        "professional fashion illustration, white background, "
        + prompt +
        ", studio lighting, clean lines, fabric texture, full outfit view"
    )

def generate_designs(prompt, n=2, out="outputs"):
    os.makedirs(out, exist_ok=True)

    paths = []

    for i in range(n):
        try:
            encoded = urllib.parse.quote(enhance_prompt(prompt))

            url = (
                f"https://image.pollinations.ai/prompt/{encoded}"
                f"?width=512&height=512&seed={i+42}&nologo=true"
            )

            print("\n" + "=" * 60)
            print("URL:", url)

            response = requests.get(url, timeout=120)

            print("STATUS:", response.status_code)
            print("CONTENT TYPE:", response.headers.get("content-type"))

            if response.status_code != 200:
                print("API ERROR")
                continue

            path = f"{out}/design_{i+1}.png"

            with open(path, "wb") as f:
                f.write(response.content)

            print("Saved:", path)
            print("Exists:", os.path.exists(path))
            print("Size:", os.path.getsize(path))

            paths.append(path)

        except Exception as e:
            print("ERROR:", repr(e))

    print("Final paths:", paths)

    return paths

def find_products(prompt, k=3):
    tags = [p["tags"] for p in PRODUCT_CATALOGUE]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([prompt] + tags)
    scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    top_indices = scores.argsort()[::-1][:k]
    return [PRODUCT_CATALOGUE[i] for i in top_indices]
