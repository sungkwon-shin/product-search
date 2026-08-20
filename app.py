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
                    
                    # 이미지 변환
                    buffered = BytesIO()
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    image.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    # [갤러리 뷰어 핵심 코드] 클릭 시 모달창(전체화면)이 뜹니다.
                    html_code = f'''
                    <style>
                    /* 1. 작은 이미지 스타일 */
                    .thumb {{ cursor: zoom-in; border-radius: 8px; width: 100%; }}
                    
                    /* 2. 전체화면 모달 (기본은 숨김) */
                    .modal {{
                        display: none; position: fixed; z-index: 9999; left: 0; top: 0;
                        width: 100%; height: 100%; background-color: rgba(0,0,0,0.9);
                        justify-content: center; align-items: center; cursor: zoom-out;
                    }}
                    /* 3. 모달 안의 이미지 */
                    .modal-content {{ max-width: 95%; max-height: 95%; object-fit: contain; }}
                    </style>

                    <!-- 이미지 클릭 시 모달 열기 -->
                    <img src="data:image/jpeg;base64,{img_str}" class="thumb" onclick="document.getElementById('myModal').style.display='flex'">

                    <!-- 모달창 -->
                    <div id="myModal" class="modal" onclick="this.style.display='none'">
                        <img class="modal-content" src="data:image/jpeg;base64,{img_str}">
                    </div>
                    '''
                    st.markdown(html_code, unsafe_allow_html=True)
                    
                    found = True
                    break
                    
        if not found:
            st.error(f"⚠️ [{product_id}] 이미지를 찾을 수 없습니다.")
    else:
        st.warning("⚠️ 검색할 품번을 입력해 주세요.")
