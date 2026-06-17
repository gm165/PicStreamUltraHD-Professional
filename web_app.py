import streamlit as np
import streamlit as st
from PIL import Image, ImageOps
from rembg import remove
import io
import zipfile

# Page Configuration (Title aur Icon)
st.set_page_config(page_title="PicStreamUltraHD Pro", page_icon="📸", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .main-title { font-size: 38px; font-weight: bold; color: #1E88E5; text-align: center; margin-bottom: 5px; }
    .sub-title { font-size: 16px; text-align: center; color: #555; margin-bottom: 30px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📸 PicStreamUltraHD Professional</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Powered by GM Tech Solutions — AI Background Remover & 19KB Optimizer</div>', unsafe_allow_html=True)

# Tabs System
tab1, tab2, tab3 = st.tabs(["🎯 Single Image Mode", "📦 Bulk / Folder Mode", "ℹ️ About Us"])

# Background Options Dictionary
bg_options = {
    "White Background": (255, 255, 255),
    "Blue Background": (0, 0, 255),
    "Green Background": (0, 255, 0),
    "Transparent": None
}

# --- FUNCTION: PROCESS IMAGE ---
def process_single_image(uploaded_file, bg_color, output_format):
    # 1. Read Image
    input_image = Image.open(uploaded_file)
    
    # 2. Remove Background using AI
    no_bg_image = remove(input_image)
    
    # 3. Apply New Background Color
    if bg_color:
        final_image = Image.new("RGBA", no_bg_image.size, bg_color + (255,))
        final_image.paste(no_bg_image, (0, 0), no_bg_image)
    else:
        final_image = no_bg_image

    # Convert to RGB if JPG
    if output_format == "JPG":
        final_image = final_image.convert("RGB")
        
    # 4. Smart 19KB Optimization (Compression Loop)
    img_byte_arr = io.BytesIO()
    quality = 95
    while quality > 10:
        img_byte_arr.seek(0)
        img_byte_arr.truncate(0)
        if output_format == "JPG":
            final_image.save(img_byte_arr, format="JPEG", quality=quality)
        else:
            final_image.save(img_byte_arr, format="PNG", compress_level=int((100-quality)/10))
            
        file_size = img_byte_arr.tell() / 1024  # Size in KB
        if file_size <= 19 or output_format == "PNG": # PNG compress loops standard strictly
            break
        quality -= 5
        
    return img_byte_arr.getvalue(), output_format.lower()

# ==================== TAB 1: SINGLE IMAGE ====================
with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Settings")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp"])
        
        bg_choice = st.selectbox("Background Mode:", list(bg_options.keys()))
        output_format = st.selectbox("Output Format:", ["JPG", "PNG"])
        
        process_btn = st.button("🚀 Process & Optimize", key="single_btn")

    with col2:
        st.subheader("Live Preview")
        if uploaded_file:
            st.image(uploaded_file, caption="Original Image", width=250)
            
            if process_btn:
                with st.spinner("AI is removing background... Please wait (First time takes 1-2 mins)"):
                    try:
                        processed_bytes, ext = process_single_image(uploaded_file, bg_options[bg_choice], output_format)
                        st.success(f"Mukammal ho gaya! Size: {len(processed_bytes)/1024:.2f} KB (Target: ≤ 19KB)")
                        
                        # Download Button
                        st.download_button(
                            label="📥 Download Output Image",
                            data=processed_bytes,
                            file_name=f"optimized_output.{ext}",
                            mime=f"image/{ext}"
                        )
                    except Exception as e:
                        st.error(f"Kuch ghalti hoi: {str(e)}")

# ==================== TAB 2: BULK MODE ====================
with tab2:
    st.subheader("📦 Bulk Processing (Upload Multiple Images)")
    uploaded_files = st.file_uploader("Select Folder Images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    col3, col4 = st.columns([1, 1])
    with col3:
        bulk_bg_choice = st.selectbox("Bulk Background:", list(bg_options.keys()), key="bulk_bg")
        bulk_format = st.selectbox("Bulk Format:", ["JPG", "PNG"], key="bulk_fmt")
    
    bulk_process_btn = st.button("⚡ Start Bulk Processing", key="bulk_btn")
    
    if uploaded_files and bulk_process_btn:
        zip_buffer = io.BytesIO()
        processed_count = 0
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for i, file in enumerate(uploaded_files):
                status_text.text(f"Processing ({i+1}/{len(uploaded_files)}): {file.name}")
                try:
                    p_bytes, ext = process_single_image(file, bg_options[bulk_bg_choice], bulk_format)
                    zip_file.writestr(f"optimized_{file.name.split('.')[0]}.{ext}", p_bytes)
                    processed_count += 1
                except Exception as e:
                    st.warning(f"File {file.name} skip ho gayi: {str(e)}")
                progress_bar.progress((i + 1) / len(uploaded_files))
                
        status_text.text("Status: Completed!")
        st.success(f"Mukammal ho gaya! {processed_count} out of {len(uploaded_files)} images process ho gayi hain.")
        
        st.download_button(
            label="📥 Download All Images (ZIP File)",
            data=zip_buffer.getvalue(),
            file_name="Optimized_Outputs.zip",
            mime="application/zip"
        )

# ==================== TAB 3: ABOUT US ====================
with tab3:
    st.markdown("""
    ### 🌟 PicStreamUltraHD Professional
    **Developed by GM Tech Solutions**
    
    Yeh aik modern cloud-based system hai jo automated school administration aur data optimization ke liye banaya gaya hai.
    * **AI Technology:** Rembg ONNX Runtime
    * **Features:** Automatic 19KB Compression, Background replacement, Bulk processing.
    """)