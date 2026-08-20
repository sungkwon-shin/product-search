import streamlit as st
import streamlit.components.v1 as components
import os
import base64
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="품번 조회 시스템", layout="centered")

# 기존 스트림릿 돋보기 기능 강제 삭제
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
                    
                    # 이미지를 웹용으로 변환
                    buffered = BytesIO()
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    image.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    # 💡 더블클릭 이벤트로 변경 및 안내 문구 수정
                    html_code = f"""
                    <div id="wrapper" style="width: 100%; height: 500px; border-radius: 8px; overflow: hidden; background-color: #f8f9fa; position: relative; display: flex; justify-content: center; align-items: center; border: 1px solid #ddd; touch-action: none;">
                        <!-- 실시간 확대 퍼센트 배지 -->
                        <div id="zoom-indicator" style="position: absolute; top: 15px; right: 15px; background-color: rgba(0, 0, 0, 0.65); color: #fff; padding: 6px 12px; border-radius: 20px; font-size: 13px; font-weight: bold; font-family: sans-serif; z-index: 10; pointer-events: none;">
                            100%
                        </div>
                        <img id="myImg" src="data:image/jpeg;base64,{img_str}" style="max-width: 100%; max-height: 100%; cursor: zoom-in;">
                    </div>
                    <p style="text-align: center; color: #555; font-size: 14px; margin-top: 10px; font-family: sans-serif; line-height: 1.6;">
                        👆 <b>사진 더블 터치(따닥!)</b>: 3배 확대 및 원상복구<br>
                        🖱️ <b>마우스 휠 / 두 손가락</b>: 자유롭게 추가 확대·축소 (최대 50배)<br>
                        🖐️ <b>드래그(스와이프)</b>: 커진 상태에서 상하좌우 이동
                    </p>
                    
                    <!-- Panzoom 라이브러리 로드 -->
                    <script src="https://cdn.jsdelivr.net/npm/@panzoom/panzoom@4.5.1/dist/panzoom.min.js"></script>
                    <script>
                        const elem = document.getElementById('myImg');
                        const wrapper = document.getElementById('wrapper');
                        const zoomIndicator = document.getElementById('zoom-indicator');
                        
                        // 줌 기능 활성화
                        const panzoom = Panzoom(elem, {{
                            maxScale: 50,
                            minScale: 1,
                            step: 1.2
                        }});

                        // PC 마우스 휠 확대/축소 연결
                        wrapper.addEventListener('wheel', panzoom.zoomWithWheel);

                        // [핵심] 더블 클릭(dblclick) 시 3배 확대 및 원상복구 로직
                        let isZoomed = false;
                        elem.addEventListener('dblclick', (e) => {{
                            if (!isZoomed) {{
                                // 더블 클릭한 마우스 위치를 중심으로 3배 확대
                                panzoom.zoomToPoint(3.0, {{ clientX: e.clientX, clientY: e.clientY }});
                                isZoomed = true;
                                elem.style.cursor = 'grab';
                            }} else {{
                                panzoom.reset();
                                isZoomed = false;
                                elem.style.cursor = 'zoom-in';
                            }}
                        }});

                        // 휠이나 손가락 핀치로 크기가 바뀌었을 때 상태 및 퍼센트 업데이트
                        elem.addEventListener('panzoomzoom', (e) => {{
                            const currentScale = e.detail.scale;
                            
                            // 배지에 현재 퍼센트 표시 (예: 1.5배 -> 150%)
                            zoomIndicator.innerText = Math.round(currentScale * 100) + '%';
                            
                            if (currentScale <= 1) {{
                                isZoomed = false;
                                elem.style.cursor = 'zoom-in';
                            }} else {{
                                isZoomed = true;
                                elem.style.cursor = 'grab';
                            }}
                        }});
                    </script>
                    """
                    
                    # 스트림릿에 커스텀 HTML 뷰어 출력
                    components.html(html_code, height=300)
                    
                    found = True
                    break
                    
        if not found:
            st.error(f"⚠️ [{product_id}] 이미지를 찾을 수 없습니다.")
    else:
        st.warning("⚠️ 검색할 품번을 입력해 주세요.")
