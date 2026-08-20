import streamlit as st
import os
from PIL import Image
from streamlit_image_zoom import image_zoom

st.set_page_config(page_title="품번 조회 시스템", layout="centered")

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
                    
                    st.success(f"✅ 품번 [{name}] 검색 완료")
                    
                    # 이미지를 안전하게 오픈
                    image = Image.open(file_path)
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                        
                    # [핵심] 안드로이드에서 화면 안에서 바로 부분 확대/이동이 가능한 전용 줌 뷰어 적용
                    # mode="dragmove": 터치하고 드래그하면 원하는 부위를 자유롭게 이동하며 확대해서 볼 수 있습니다.
                    image_zoom(
                        image, 
                        mode="dragmove", 
                        size=(600, 600), 
                        zoom_factor=2.5, 
                        keep_aspect_ratio=True
                    )
                    
                    found = True
                    break
                    
        if not found:
            st.error(f"⚠️ [{product_id}] 이미지를 찾을 수 없습니다.")
    else:
        st.warning("⚠️ 검색할 품번을 입력해 주세요.")
