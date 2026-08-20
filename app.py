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
                    
                    # 이미지를 웹용으로 변환
                    buffered = BytesIO()
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    image.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    # 지저분한 버튼 하나 없이 깔끔하게 동작하는 프로페셔널 뷰어 엔진 탑재
                    html_code = f'''
                    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/viewerjs/1.11.6/viewer.min.css">
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/viewerjs/1.11.6/viewer.min.js"></script>

                    <div style="text-align: center;">
                        <img id="product-img" src="data:image/jpeg;base64,{img_str}" style="width: 100%; border-radius: 8px; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        <p style="color: gray; font-size: 14px; margin-top: 10px;">
                            👆 사진을 터치하면 전체 화면으로 열립니다.<br>
                            (두 손가락으로 확대/축소, 한 번 가볍게 톡! 치면 닫힘)
                        </p>
                    </div>

                    <script>
                    const image = document.getElementById('product-img');
                    const viewer = new Viewer(image, {{
                        button: false,   // 닫기 버튼 없앰 (클릭으로 닫을 거니까)
                        navbar: false,   // 하단 썸네일 없앰
                        title: false,    // 제목 글씨 없앰
                        toolbar: false,  // 확대/축소 아이콘 툴바 없앰
                        tooltip: false,  // 줌 비율 알림 없앰
                        backdrop: true,  // 배경 까맣게
                        viewed() {{
                            // 모바일/PC 모두 '드래그(줌)'와 '클릭(닫기)'을 똑똑하게 구분하는 로직
                            const canvas = document.querySelector('.viewer-canvas');
                            let startX, startY;
                            
                            // PC 마우스용
                            canvas.addEventListener('mousedown', (e) => {{
                                startX = e.clientX;
                                startY = e.clientY;
                            }});
                            canvas.addEventListener('mouseup', (e) => {{
                                if (Math.abs(e.clientX - startX) < 5 && Math.abs(e.clientY - startY) < 5) viewer.hide();
                            }});

                            // 스마트폰 터치용
                            canvas.addEventListener('touchstart', (e) => {{
                                if (e.touches.length === 1) {{
                                    startX = e.touches[0].clientX;
                                    startY = e.touches[0].clientY;
                                }}
                            }}, {{ passive: true }});
                            canvas.addEventListener('touchend', (e) => {{
                                if (e.changedTouches.length === 1) {{
                                    if (Math.abs(e.changedTouches[0].clientX - startX) < 10 && Math.abs(e.changedTouches[0].clientY - startY) < 10) viewer.hide();
                                }}
                            }});
                        }}
                    }});
                    </script>
                    '''
                    st.markdown(html_code, unsafe_allow_html=True)
                    
                    found = True
                    break
                    
        if not found:
            st.error(f"⚠️ [{product_id}] 이미지를 찾을 수 없습니다.")
    else:
        st.warning("⚠️ 검색할 품번을 입력해 주세요.")
