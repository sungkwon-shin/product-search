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
                    
                    # 닫기 오류를 완벽하게 해결하고 스마트폰 주소창까지 덮는 '진짜 전체창' 기능 추가
                    html_code = f'''
                    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/viewerjs/1.11.6/viewer.min.css">
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/viewerjs/1.11.6/viewer.min.js"></script>

                    <div style="text-align: center;">
                        <img id="product-img" src="data:image/jpeg;base64,{img_str}" style="width: 100%; border-radius: 8px; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        <p style="color: gray; font-size: 14px; margin-top: 10px;">
                            👆 사진을 터치하면 <b>스마트폰 전체창</b>으로 꽉 차게 확대됩니다.<br>
                            (손가락으로 확대/축소 가능, 가볍게 한 번 '톡' 치면 닫힘)
                        </p>
                    </div>

                    <script>
                    const image = document.getElementById('product-img');
                    
                    const viewer = new Viewer(image, {{
                        button: false,
                        navbar: false,
                        title: false,
                        toolbar: false,
                        tooltip: false,
                        backdrop: true,
                        show() {{
                            // 사진이 열릴 때 스마트폰 주소창까지 완전히 가려버리는 '전체화면' 요청
                            const docElm = document.documentElement;
                            if (docElm.requestFullscreen) docElm.requestFullscreen().catch(()=>{{}});
                            else if (docElm.webkitRequestFullscreen) docElm.webkitRequestFullscreen();
                        }},
                        viewed() {{
                            const canvas = document.querySelector('.viewer-canvas');
                            let startX = 0, startY = 0, startTime = 0;
                            let isMultiTouch = false; // 두 손가락 터치(줌) 방어용
                            
                            // [핵심] 모바일 터치 '닫기' 완벽 감지 로직
                            canvas.addEventListener('touchstart', (e) => {{
                                if (e.touches.length > 1) {{
                                    isMultiTouch = true; // 손가락이 2개 이상이면 줌(확대) 상태로 인식
                                }} else if (e.touches.length === 1) {{
                                    isMultiTouch = false;
                                    startX = e.touches[0].clientX;
                                    startY = e.touches[0].clientY;
                                    startTime = Date.now();
                                }}
                            }}, {{ passive: true }});
                            
                            canvas.addEventListener('touchend', (e) => {{
                                if (isMultiTouch) return; // 줌 하던 중이었으면 닫지 않음
                                
                                if (e.changedTouches.length === 1) {{
                                    let diffX = Math.abs(e.changedTouches[0].clientX - startX);
                                    let diffY = Math.abs(e.changedTouches[0].clientY - startY);
                                    let diffTime = Date.now() - startTime;
                                    
                                    // 0.3초 이내로, 손가락을 거의 움직이지 않고 '톡' 쳤을 때만 닫기 실행
                                    if (diffX < 15 && diffY < 15 && diffTime < 300) {{
                                        viewer.hide();
                                    }}
                                }}
                            }});

                            // PC 마우스 '닫기' 완벽 감지 로직
                            canvas.addEventListener('mousedown', (e) => {{
                                startX = e.clientX;
                                startY = e.clientY;
                                startTime = Date.now();
                            }});
                            canvas.addEventListener('mouseup', (e) => {{
                                let diffX = Math.abs(e.clientX - startX);
                                let diffY = Math.abs(e.clientY - startY);
                                let diffTime = Date.now() - startTime;
                                
                                if (diffX < 10 && diffY < 10 && diffTime < 400) {{
                                    viewer.hide();
                                }}
                            }});
                        }},
                        hidden() {{
                            // 사진이 닫힐 때 전체창 모드도 같이 종료됨
                            if (document.fullscreenElement) document.exitFullscreen().catch(()=>{{}});
                            else if (document.webkitFullscreenElement) document.webkitExitFullscreen();
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
