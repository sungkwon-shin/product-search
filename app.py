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
                    
                    # 이미지를 안전하게 표준 웹 포맷으로 변환
                    buffered = BytesIO()
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    image.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    # [핵심] PC와 안드로이드 모두에서 완벽하게 새 창을 띄우는 브라우저 표준 HTML 태그
                    html_code = f'''
                    <div style="text-align: center; margin-top: 10px;">
                        <a href="data:image/jpeg;base64,{img_str}" target="_blank" style="display: block; cursor: zoom-in;">
                            <img src="data:image/jpeg;base64,{img_str}" style="width: 100%; max-width: 500px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        </a>
                        <p style="color: #666; font-size: 14px; margin-top: 12px;">
                            👆 <b>사진을 클릭(터치)하면 새 창으로 크게 열립니다.</b><br>
                            (PC: 마우스 휠/새 창 확대 | 안드로이드: 두 손가락 줌 / 뒤로 가기로 닫기)
                        </p>
                    </div>
                    '''
                    st.markdown(html_code, unsafe_allow_html=True)
                    
                    found = True
                    break
                    
        if not found:
            st.error(f"⚠️ [{product_id}] 이미지를 찾을 수 없습니다.")
    else:
        st.warning("⚠️ 검색할 품번을 입력해 주세요.")
