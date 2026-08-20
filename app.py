import streamlit as st
import os
from PIL import Image

st.set_page_config(page_title="품번 조회 시스템", layout="centered")

st.title("📦 품번 이미지 조회 시스템")
st.markdown("조회할 제품의 품번을 입력해 주세요.")

IMAGE_FOLDER = "images" 

# 안내 문구도 대소문자 상관없다는 것을 명시
product_id = st.text_input("🔍 품번 입력", placeholder="예: a123 또는 A123")

if st.button("이미지 검색", use_container_width=True):
    if product_id:
        # 1. 사용자가 입력한 검색어를 무조건 소문자로 싹 변환하고 공백 제거
        search_term = product_id.strip().lower()
        found = False
        
        # 2. 이미지 폴더 안의 모든 사진을 하나씩 검사
        if os.path.exists(IMAGE_FOLDER):
            for filename in os.listdir(IMAGE_FOLDER):
                # 파일 이름과 확장자를 분리 (예: 'A123'과 '.jpg')
                name, ext = os.path.splitext(filename)
                
                # 3. 사진 이름도 무조건 소문자로 바꿔서 검색어와 비교! 
                if name.lower() == search_term and ext.lower() in ['.jpg', '.jpeg', '.png']:
                    file_path = os.path.join(IMAGE_FOLDER, filename)
                    image = Image.open(file_path)
                    
                    # 화면에 보여줄 때는 원래 사진 이름(대소문자 유지)으로 출력
                    st.success(f"✅ 품번 [{name}] 검색 완료")
                    st.image(image, caption=f"품번: {name}", use_container_width=True)
                    found = True
                    break
                    
        if not found:
            st.error(f"⚠️ [{product_id}] 이미지를 찾을 수 없습니다.")
    else:
        st.warning("⚠️ 검색할 품번을 입력해 주세요.")
