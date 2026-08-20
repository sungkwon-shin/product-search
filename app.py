import streamlit as st
import os
from PIL import Image

st.set_page_config(page_title="품번 조회 시스템", layout="centered")

st.title("📦 품번 이미지 조회 시스템")
st.markdown("조회할 제품의 품번을 입력해 주세요.")

IMAGE_FOLDER = "images" 

product_id = st.text_input("🔍 품번 입력", placeholder="예: A123")

if st.button("이미지 검색", use_container_width=True):
    if product_id:
        clean_id = product_id.strip()
        found = False
        extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.PNG']
        
        for ext in extensions:
            file_path = os.path.join(IMAGE_FOLDER, f"{clean_id}{ext}")
            
            if os.path.exists(file_path):
                image = Image.open(file_path)
                st.success(f"✅ 품번 [{clean_id}] 검색 완료")
                st.image(image, caption=f"품번: {clean_id}", use_container_width=True)
                found = True
                break
                
        if not found:
            st.error(f"⚠️ [{clean_id}] 이미지를 찾을 수 없습니다.")
    else:
        st.warning("⚠️ 검색할 품번을 입력해 주세요.")