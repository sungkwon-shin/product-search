import streamlit as st
import os
import base64
from io import BytesIO
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
                    image = Image.open(file_path)
                    
                    st.success(f"✅ 품번 [{name}] 검색 완료")
                    
                    # 이미지를 변환
                    buffered = BytesIO()
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    image.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    # 자바스크립트 없이 CSS(체크박스 해킹 기법)만으로 터치 확대/축소 완벽 구현
                    html_code = f'''
                        <style>
                        .zoom-checkbox {{ display: none; }}
                        .zoom-img {{
                            width: 100%;
                            cursor: zoom-in;
                            border-radius: 8px;
                            transition: 0.3s;
                            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                        }}
                        /* 사진이 터치되었을 때(체크박스가 켜졌을 때) 화면 꽉 차게 만들기 */
                        .zoom-checkbox:checked ~ .zoom-img {{
                            position: fixed;
                            top: 0;
                            left: 0;
                            width: 100vw;
                            height: 100vh;
                            object-fit: contain;
                            background-color: rgba(0,0,0,0.95);
                            z-index: 999999;
                            cursor: zoom-out;
                            padding: 0;
                            margin: 0;
                        }}
                        </style>
                        
                        <label style="display: block; width: 100%; margin: 0;">
                            <input type="checkbox" class="zoom-checkbox">
                            <img src="data:image/jpeg;base64,{img_str}" class="zoom-img">
                        </label>
                        
                        <p style="text-align: center; color: gray; font-size: 14px; margin-top: 15px;">
                            👆 사진을 터치하면 화면 가득 확대됩니다. (다시 누르면 원상복구)
                        </p>
                    '''
                    st.markdown(html_code, unsafe_allow_html=True)
                    
                    found = True
                    break
                    
        if not found:
            st.error(f"⚠️ [{product_id}] 이미지를 찾을 수 없습니다.")
    else:
        st.warning("⚠️ 검색할 품번을 입력해 주세요.")
