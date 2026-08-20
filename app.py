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
                    
                    # 이미지를 웹용으로 변환
                    buffered = BytesIO()
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    image.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    # [핵심] 안드로이드 차단을 무시하고 두 손가락 확대를 강제로 실행하는 전문 갤러리 엔진
                    html_code = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                      <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5, user-scalable=yes">
                      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/viewerjs/1.11.3/viewer.min.css">
                      <style>
                        body {{ margin: 0; display: flex; justify-content: center; background-color: transparent; }}
                        .img-container {{ width: 100%; cursor: pointer; }}
                        img {{ width: 100%; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                      </style>
                    </head>
                    <body>
                      <div class="img-container">
                        <img id="image" src="data:image/jpeg;base64,{img_str}">
                      </div>
                      
                      <!-- 전 세계적으로 쓰이는 검증된 줌(Zoom) 라이브러리 탑재 -->
                      <script src="https://cdnjs.cloudflare.com/ajax/libs/viewerjs/1.11.3/viewer.min.js"></script>
                      <script>
                        const viewer = new Viewer(document.getElementById('image'), {{
                          inline: false,
                          toolbar: false,
                          navbar: false,
                          title: false,
                          button: true,    // 우측 상단 닫기(X) 버튼 생성
                          backdrop: true,  // 검은 배경 생성
                          zoomable: true,  // 두 손가락 핀치 줌 완벽 지원!
                          movable: true,   // 드래그 이동 지원
                          transition: true
                        }});
                      </script>
                    </body>
                    </html>
                    """
                    
                    # 뷰어가 잘 작동하도록 넉넉한 공간(높이 550)을 할당
                    components.html(html_code, height=550)
                    
                    st.info("👆 사진을 터치하면 갤러리가 열립니다. 열린 상태에서 스마트폰 화면을 두 손가락으로 자유롭게 확대/축소하세요.")
                    found = True
                    break
                    
        if not found:
            st.error(f"⚠️ [{product_id}] 이미지를 찾을 수 없습니다.")
    else:
        st.warning("⚠️ 검색할 품번을 입력해 주세요.")
