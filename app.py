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
                    
                    # 이미지를 웹용 Base64 데이터로 변환
                    buffered = BytesIO()
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    image.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    # [핵심] 스트림릿의 방해를 피해, 부모 창(전체 화면)에 순수 HTML 레이어를 띄우는 코드
                    components.html(f'''
                    <div style="text-align: center; font-family: sans-serif;">
                        <img src="data:image/jpeg;base64,{img_str}" 
                             style="width: 100%; border-radius: 8px; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" 
                             onclick="openLayer()">
                        <p style="color: gray; font-size: 14px; margin-top: 15px;">
                            👆 사진을 터치하면 <b>전체화면 레이어</b>로 열립니다.
                        </p>
                    </div>

                    <script>
                    function openLayer() {{
                        const parentDoc = window.parent.document;
                        
                        // 1. 모바일 기기에서 두 손가락 확대(Zoom)를 강제로 허용
                        let meta = parentDoc.querySelector('meta[name="viewport"]');
                        if (meta) {{
                            meta.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes');
                        }}

                        // 2. 혹시 열려있는 기존 레이어가 있으면 깔끔하게 지움
                        let existingLayer = parentDoc.getElementById('custom-viewer-layer');
                        if(existingLayer) existingLayer.remove();

                        // 3. 스트림릿 화면 전체를 덮는 까만색 순수 HTML 레이어 생성
                        const overlay = parentDoc.createElement('div');
                        overlay.id = 'custom-viewer-layer';
                        overlay.style.position = 'fixed';
                        overlay.style.top = '0';
                        overlay.style.left = '0';
                        overlay.style.width = '100vw';
                        overlay.style.height = '100vh';
                        overlay.style.backgroundColor = 'rgba(0,0,0,0.95)';
                        overlay.style.zIndex = '999999'; // 무조건 제일 위로
                        overlay.style.display = 'flex';
                        overlay.style.justifyContent = 'center';
                        overlay.style.alignItems = 'center';
                        overlay.style.overflow = 'auto'; 

                        // 4. 레이어 안에 들어갈 원본 이미지 설정
                        const img = parentDoc.createElement('img');
                        img.src = 'data:image/jpeg;base64,{img_str}';
                        img.style.maxWidth = '100%';
                        img.style.maxHeight = '100%';
                        img.style.objectFit = 'contain';

                        // 5. 레이어 아무 곳이나 터치하면 다시 닫히도록 설정 (터치 충돌 없음!)
                        overlay.onclick = function() {{
                            overlay.remove();
                        }};

                        // 6. 화면에 최종 부착
                        overlay.appendChild(img);
                        parentDoc.body.appendChild(overlay);
                    }}
                    </script>
                    ''', height=450)
                    
                    found = True
                    break
                    
        if not found:
            st.error(f"⚠️ [{product_id}] 이미지를 찾을 수 없습니다.")
    else:
        st.warning("⚠️ 검색할 품번을 입력해 주세요.")
