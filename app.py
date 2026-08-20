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
                    
                    # 이미지를 웹용 Base64로 변환하여 안드로이드 브라우저 뷰어로 직행
                    buffered = BytesIO()
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    image.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    html_code = f'''
                    <div style="text-align: center;">
                        <a href="data:image/jpeg;base64,{img_str}" target="_blank" style="text-decoration: none;">
                            <img src="data:image/jpeg;base64,{img_str}" style="width: 100%; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        </a>
                        <p style="color: gray; font-size: 14px; margin-top: 15px; line-height: 1.5;">
                            👆 사진을 터치하면 <b>안드로이드 원본 뷰어</b>로 열립니다.<br>
                            (두 손가락으로 자유롭게 확대/축소 하시고, <b>'뒤로 가기'</b>를 누르면 닫힙니다)
                        </p>
                    </div>
                    '''
                    st.markdown(html_code, unsafe_allow_html=True)
                    
                    found = Type = True
                    found = True
                    break
                    
        if not found:
            st.error(f"⚠️ [{product_id}] 이미지를 찾을 수 없습니다.")
    else:
        st.warning("⚠️ 검색할 품번을 입력해 주세요.")
