import streamlit as st
import os
from fashion_ai import generate_designs, find_products

st.set_page_config(
    page_title="AI Fashion Designer",
    page_icon="👗",
    layout="wide"
)

st.title("👗 AI Fashion Design Studio")
st.caption("Describe any outfit and generate AI fashion concepts instantly.")

# Sidebar

with st.sidebar:
    st.header("⚙️ Settings")
    num_variants = st.slider("Design Variants", 1, 3, 2)
    num_products = st.slider("Product Suggestions", 1, 5, 3)

# Input

prompt = st.text_input(
"Describe your outfit idea 👇",
placeholder="e.g. modern floral summer dress with pastel colors"
)

# Generate Button

if st.button("✨ Generate", use_container_width=True):
    if not prompt.strip():
        st.warning("Please enter a design description.")
        st.stop()
    
    try:
        with st.spinner("🎨 Generating fashion designs..."):
            paths = generate_designs(
                prompt=prompt,
                n=num_variants
            )
    
        valid_paths = [
            p for p in paths
            if os.path.exists(p)
        ]
    
        if valid_paths:
    
            st.success(
                f"Successfully generated {len(valid_paths)} design(s)."
            )
    
            st.subheader("🎨 AI Generated Designs")
    
            cols = st.columns(len(valid_paths))
    
            for idx, (col, img_path) in enumerate(
                zip(cols, valid_paths),
                start=1
            ):
                with col:
                    st.image(
                        img_path,
                        caption=f"Variant {idx}",
                        use_container_width=True
                    )
    
        else:
            st.error(
                "No images were generated. Check the terminal logs for details."
            )
    
        st.divider()
    
        st.subheader("🛍️ Similar Affordable Products")
    
        products = find_products(
            prompt,
            k=num_products
        )
    
        if products:
    
            cols = st.columns(len(products))
    
            for col, product in zip(cols, products):
    
                with col:
                    st.markdown(
                        f"### {product['name']}"
                    )
    
                    st.markdown(
                        f"🏷️ {product['price']}"
                    )
    
                    st.markdown(
                        f"🏪 {product['brand']}"
                    )
    
                    st.link_button(
                        "Shop Now →",
                        product["url"]
                    )
    
        else:
            st.info(
                "No matching products found."
            )

    except Exception as e:
        st.exception(e)

