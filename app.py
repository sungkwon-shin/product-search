import streamlit as st
import os
from PIL import Image

st.set_page_config(page_title="품번 조회 시스템", layout="centered")

# 핵심 해결책: 우측 상단의 쪼그만 '확대 버튼'을 사진 전체 크기로 늘려서 투명하게 덮어버립니다.
st.markdown("""
    <style>
    button[title="View fullscreen"], [data-testid="StyledFullScreenButton"] {
        width: 100% !important;
        height: 100% !important;
        top: 0 !important;
        left: 0 !important;
        position: absolute !important;
        opacity: 0 !important; 
        z-index: 99 !important;
        display: block !important;
        visibility: visible !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📦 품번 이미지 조회 시스템")
st.markdown("조회할 제품의 품번을 입력해 주세요.")

IMAGE_FOLDER = "images" 

with st.form(key="search_form"):
    product_id = st.text_input("🔍 품번 입력", placeholder="예: a123 또는 A123")
    submit_button = st.form_submit_button("이미지 검색", use_container_width=True)

if submit_button:
    if product_id:
        search_term = product_id.strip().lower()
        found = False
        
        if os.path.exists(IMAGE_FOLDER):
            for filename in os.listdir(IMAGE_FOLDER):
                name, ext = os.path.splitext(filename)
                
                if name.lower() == search_term and ext.lower() in ['.jpg', '.jpeg', '.png']:
                    file_path = os.path.join(IMAGE_FOLDER, filename)
                    image = Image.open(file_path)
                    
                    st.success(f"✅ 품번 [{name}] 검색 완료")
                    
                    # 사진 출력 (보이지 않는 거대한 확대 버튼이 사진을 덮고 있습니다)
                    st.image(image, caption="👆 사진 아무 곳이나 터치하면 전체 화면으로 꽉 차게 확대됩니다.", use_container_width=True)
                    
                    found = True
                    break
                    
        if not found:
            st.error(f"⚠️ [{product_id}] 이미지를 찾을 수 없습니다.")
    else:
        st.warning("⚠️ 검색할 품번을 입력해 주세요.")
