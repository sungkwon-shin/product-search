import streamlit as st
import streamlit.components.v1 as components
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
                    
                    # 이미지를 Base64로 변환
                    buffered = BytesIO()
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    image.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    # 스트림릿 감옥을 우회하여 화면 전체를 덮는 HTML/JS 레이어 삽입
                    components.html(f'''
                    <div style="text-align: center; font-family: sans-serif;">
                        <img id="target-img" src="data:image/jpeg;base64,{img_str}" 
                             style="width: 100%; border-radius: 8px; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        <p style="color: gray; font-size: 13px; margin-top: 10px;">
                            👆 사진을 터치하면 <b>팝업 레이어</b>가 열립니다.
                        </p>
                    </div>

                    <script>
                    const imgElement = document.getElementById('target-img');
                    
                    imgElement.onclick = function() {{
                        const parentDoc = window.parent.document;
                        
                        // 1. 기존 레이어가 있으면 삭제
                        let oldLayer = parentDoc.getElementById('html-lightbox');
                        if (oldLayer) oldLayer.remove();
                        
                        // 2. HTML과 똑같은 방식의 풀스크린 레이어 생성
                        const overlay = parentDoc.createElement('div');
                        overlay.id = 'html-lightbox';
                        overlay.style.position = 'fixed';
                        overlay.style.top = '0';
                        overlay.style.left = '0';
                        overlay.style.width = '100vw';
                        overlay.style.height = '100vh';
                        overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.95)';
                        overlay.style.zIndex = '9999999';
                        overlay.style.display = 'flex';
                        overlay.style.justifyContent = 'center';
                        overlay.style.alignItems = 'center';
                        overlay.style.overflow = 'auto';

                        // 3. 레이어 안의 이미지 (두 손가락 확대/축소 가능하도록 설정)
                        const bigImg = parentDoc.createElement('img');
                        bigImg.src = 'data:image/jpeg;base64,{img_str}';
                        bigImg.style.maxWidth = '100%';
                        bigImg.style.maxHeight = '100%';
                        bigImg.style.objectFit = 'contain';
                        bigImg.style.touchAction = 'pinch-zoom'; // 안드로이드 핀치 줌 허용

                        // 4. 사진이나 배경을 터치하면 레이어가 닫힘 (HTML과 동일)
                        overlay.onclick = function() {{
                            overlay.remove();
                        }};

                        overlay.appendChild(bigImg);
                        parentDoc.body.appendChild(overlay);
                    }};
                    </script>
                    ''', height=400)
                    
                    found = True
                    break
                    
        if not found:
            st.error(f"⚠️ [{product_id}] 이미지를 찾을 수 없습니다.")
    else:
        st.warning("⚠️ 검색할 품번을 입력해 주세요.")
