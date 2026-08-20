import streamlit as st
import os
from PIL import Image

st.set_page_config(page_title="품번 조회 시스템", layout="centered")

# [핵심] 처음에 잘 작동했던 돋보기 아이콘을 사진 전체 크기로 늘려서 투명하게 덮습니다.
# 이제 구석을 조준할 필요 없이, 사진 아무 곳이나 툭 치면 시원하게 열립니다.
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
                    
                    # 가장 에러 없고 안정적이었던 처음 방식 그대로 출력합니다.
                    st.image(image, caption="👆 사진 아무 곳이나 터치하면 전체 화면으로 열립니다. (두 손가락 확대 가능)", use_container_width=True)
                    
                    found = True
                    break
                    
        if not found:
            st.error(f"⚠️ [{product_id}] 이미지를 찾을 수 없습니다.")
    else:
        st.warning("⚠️ 검색할 품번을 입력해 주세요.")
