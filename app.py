import streamlit as st
import os
from PIL import Image

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
                    
                    # 1. 화면에 기본 이미지를 보여줍니다
                    image = Image.open(file_path)
                    st.image(image, caption=f"품번: {name}", use_container_width=True)
                    
                    # 2. [핵심] 안드로이드 갤러리 앱을 호출하기 위한 버튼
                    with open(file_path, "rb") as file:
                        st.download_button(
                            label="🔍 갤러리 앱에서 크게 보기 (터치)",
                            data=file,
                            file_name=filename,
                            mime="image/jpeg",
                            use_container_width=True
                        )
                    
                    found = True
                    break
                    
        if not found:
            st.error(f"⚠️ [{product_id}] 이미지를 찾을 수 없습니다.")
    else:
        st.warning("⚠️ 검색할 품번을 입력해 주세요.")
