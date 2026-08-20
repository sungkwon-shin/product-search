import streamlit as st
import os
import base64
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="품번 조회 시스템", layout="centered")

# 스트림릿의 기본 '전체화면 돋보기 버튼'을 아예 보이지 않게 삭제합니다.
st.markdown("""
    <style>
    button[title="View fullscreen"] { display: none !important; }
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
                    
                    # 이미지를 변환 (HTML에서 마음대로 크기 조절을 하기 위함)
                    buffered = BytesIO()
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    image.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    # 사진을 클릭하면 그 자리에서 2.5배(250%) 커지는 기능
                    html_code = f'''
                        <style>
                        .zoom-container {{
                            width: 100%;
                            overflow: auto; /* 커졌을 때 밀어서 볼 수 있게 스크롤 생성 */
                            border-radius: 8px;
                            margin-top: 10px;
                        }}
                        .zoom-checkbox {{ display: none; }}
                        .zoom-img {{
                            width: 100%;
                            cursor: zoom-in;
                            transition: width 0.3s ease-in-out;
                            display: block;
                        }}
                        /* 사진이 터치되었을 때 폭을 2.5배로 쫙 늘림 */
                        .zoom-checkbox:checked ~ .zoom-img {{
                            width: 250%; 
                            max-width: none;
                            cursor: zoom-out;
                        }}
                        </style>
                        
                        <div class="zoom-container">
                            <label style="margin: 0; padding: 0; display: block; width: 100%;">
                                <input type="checkbox" class="zoom-checkbox">
                                <img src="data:image/jpeg;base64,{img_str}" class="zoom-img">
                            </label>
                        </div>
                        
                        <p style="text-align: center; color: gray; font-size: 14px; margin-top: 15px;">
                            👆 사진을 터치하면 그 자리에서 <b>2.5배 확대</b>됩니다.<br>(확대 후 손가락으로 밀어서 볼 수 있습니다)
                        </p>
                    '''
                    st.markdown(html_code, unsafe_allow_html=True)
                    
                    found = True
                    break
                    
        if not found:
            st.error(f"⚠️ [{product_id}] 이미지를 찾을 수 없습니다.")
    else:
        st.warning("⚠️ 검색할 품번을 입력해 주세요.")
