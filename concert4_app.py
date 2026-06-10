"""
Concert Playground Pro — Mega Artist Pool & 8 Genres Version
==========================================================
실행: streamlit run concert_survey_app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ── 1. 페이지 및 테마 설정 ──────────────────────────────
st.set_page_config(
    page_title="Concert Playground Ultimate",
    page_icon="🎤",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { 
    font-family: 'Pretendard', sans-serif; 
    background-color: #f8fafc !important; 
    color: #1e293b; 
}
.stApp { background-color: #f8fafc !important; }

/* 섹션 타이틀 */
.section-lbl {
    font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem;
    letter-spacing: 0.2em; text-transform: uppercase; color: #6366f1; margin-bottom: 0.4rem;
}
.section-ttl {
    font-size: 2rem; font-weight: 700; color: #0f172a; line-height: 1.2; margin-bottom: 1.5rem;
}
.section-ttl em { color: #10b981; font-style: normal; }

/* 커스텀 카드 */
.custom-card {
    background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px;
    padding: 1.6rem; margin-bottom: 1.2rem; height: 100%;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04), 0 2px 4px -1px rgba(0, 0, 0, 0.02);
}

/* 영수증 박스 */
.receipt-box {
    background: linear-gradient(135deg, #f0fdf4, #ffffff);
    border: 2px dashed #10b981; border-radius: 16px; padding: 1.8rem;
    margin-bottom: 2rem; box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.1);
}

.ticket-btn {
    display: inline-block; background-color: #6366f1; color: white !important; 
    padding: 0.5rem 1rem; border-radius: 8px; text-decoration: none !important; 
    font-size: 0.85rem; font-weight: 600; margin-top: 10px;
}
.ticket-btn:hover { background-color: #4f46e5; }

.survey-header {
    background: linear-gradient(135deg, #f1f5f9, #ffffff);
    border: 1px solid #cbd5e1; border-radius: 12px; padding: 1.2rem; margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)


# ── 2. [확장] 8대 장르 및 16개 아티스트 큐레이션 풀 매핑 ───────────────────
# 예산 필터링이 정상 작동하도록 각 장르별로 가성비(중저가) / 프리미엄(고가) 라인업을 배치했습니다.
recommend_pool = {
    "K-POP / 아이돌": [
        {"name": "NewJeans (뉴진스)", "cost": 130, "tag": "티켓링크 타겟 추천", "desc": "감각적인 Y2K 팝 사운드와 독보적인 무대 연출. 전 세대를 아우르는 트렌디 팝 스포트라이트.", "img": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?q=80&w=600", "url": "https://www.ticketlink.co.kr"},
        {"name": "세븐틴 (SEVENTEEN)", "cost": 160, "tag": "인터파크 최다 매진", "desc": "압도적인 에너지의 대규모 스타디움 라이브 퍼포먼스. 지칠 줄 모르는 무한 무대 스태미나.", "img": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=600", "url": "https://ticket.interpark.com"}
    ],
    "밴드 / 록 / 인디": [
        {"name": "실리카겔 (Silica Gel)", "cost": 80, "tag": "예스24 인디 차트 1위", "desc": "가장 뜨거운 인디 씬의 주역. 폭발적인 기타 사운드와 미디어 아트의 시각적 카타르시스.", "img": "https://images.unsplash.com/photo-1501386761578-eac5c94b800a?q=80&w=600", "url": "https://ticket.yes24.com"},
        {"name": "데이식스 (DAY6)", "cost": 110, "tag": "멜론티켓 예매 폭주", "desc": "전석 올스탠딩으로 완성되는 떼창의 교과서. 가슴을 울리는 감성 충만 K-밴드의 아이콘.", "img": "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?q=80&w=600", "url": "https://ticket.melon.com"}
    ],
    "힙합 / R&B": [
        {"name": "잔나비", "cost": 95, "tag": "레트로 감성 R&B/록", "desc": "독보적인 음색과 빈티지한 아날로그 감성 멜로디로 관객들을 위로하는 시적인 단독 콘서트.", "img": "https://images.unsplash.com/photo-1487180142328-054b783fc471?q=80&w=600", "url": "https://ticket.interpark.com"},
        {"name": "박재범 (Jay Park)", "cost": 120, "tag": "AOMG & More Vision 파티", "desc": "세련된 R&B 보컬과 국힙 아티스트들이 총출동하는 열정적인 스탠딩 힙합 축제.", "img": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?q=80&w=600", "url": "https://ticket.melon.com"}
    ],
    "EDM / 대형 페스티벌": [
        {"name": "S2O KOREA (송크란 페스티벌)", "cost": 140, "tag": "여름 워터 뮤직 대축제", "desc": "강렬한 EDM 비트와 십만 리터의 물줄기가 쏟아지는 아시아 최대 규모의 테마 워터 페스티벌.", "img": "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?q=80&w=600", "url": "https://www.ticketlink.co.kr"},
        {"name": "울트라 코리아 (UMF)", "cost": 190, "tag": "글로벌 헤드라이너 총집출", "desc": "세계 최정상 TOP DJ 라인업과 화려한 특수효과가 잠실 벌을 채우는 정통 전자음악의 메카.", "img": "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?q=80&w=600", "url": "https://ticket.yes24.com"}
    ],
    "뮤지컬 / 극장 연극": [
        {"name": "뮤지컬 <시카고>", "cost": 100, "tag": "스테디셀러 띵작", "desc": "재즈 오케스트라의 라이브 선율과 매혹적인 앙상블 댄스가 돋보이는 브로드웨이 정통 오리지널리티.", "img": "https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?q=80&w=600", "url": "https://ticket.interpark.com"},
        {"name": "뮤지컬 <레미제라블>", "cost": 140, "tag": "초호화 캐스팅 라인업", "desc": "웅장한 무대 장치와 대한민국 최고 명품 배우들의 감동적인 성량으로 꽉 채운 대형 명작 무대.", "img": "https://images.unsplash.com/photo-1460723237483-7a6dc9d0b212?q=80&w=600", "url": "https://ticket.interpark.com"}
    ],
    "클래식 / 오케스트라": [
        {"name": "지브리 캔들라이트 콘서트", "cost": 65, "tag": "감성 가득 가성비 추천", "desc": "수천 개의 촛불 속에서 현악 4중주로 재해석되는 인생의 회전목마 등 지브리 애니메이션 명곡선.", "img": "https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?q=80&w=600", "url": "https://ticket.interpark.com"},
        {"name": "조성진 피아노 리사이틀", "cost": 150, "tag": "예스24 클래식 전체 1위", "desc": "피아노의 거장이 선사하는 완벽한 정적과 소리의 파도. 예술의전당 콘서트홀 음향 감동의 정수.", "img": "https://images.unsplash.com/photo-1552422535-c45813c61732?q=80&w=600", "url": "https://ticket.yes24.com"}
    ],
    "재즈 / 블루스 / 소울": [
        {"name": "서울 재즈 페스티벌 (서재페)", "cost": 170, "tag": "봄날의 잔디밭 피크닉", "desc": "국내외 정상급 팝/재즈 아티스트들을 한자리에서 만나며 와인과 함께 즐기는 도심 속 휴식 페스티벌.", "img": "https://images.unsplash.com/photo-1511192336575-5a79af67a629?q=80&w=600", "url": "https://ticket.interpark.com"}
    ],
    "해외 아티스트 내한": [
        {"name": "오아시스 (Oasis) 내한 콘서트", "cost": 150, "tag": "역사적인 재결합 투어", "desc": "영국 록의 전설 오아시스의 기적적인 재결합 스타디움 투어 한국 상륙. 'Don't Look Back In Anger' 역대급 떼창 예고.", "img": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?q=80&w=600", "url": "https://ticket.interpark.com"},
        {"name": "콜드플레이 (Coldplay) 월드투어", "cost": 180, "tag": "빛과 우주의 무대 연출", "desc": "환경 친화적 키네틱 스테이지와 링 형태의 화려한 화약 레이저 연출, 관객 반응형 원격 LED 팔찌가 선사하는 전율.", "img": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?q=80&w=600", "url": "https://ticket.interpark.com"},
        {"name": "브루노 마스 (Bruno Mars) 라이브", "cost": 210, "tag": "소울/펑크 완벽 끝판왕", "desc": "단 1초도 쉴 틈 없는 정통 브라스 밴드 세션과 브루노 마스의 천재적인 하이노트 보컬 퍼포먼스 쇼.", "img": "https://images.unsplash.com/photo-1484755560695-a4c748918c29?q=80&w=600", "url": "https://ticket.interpark.com"}
    ]
}

# 25건의 실제 예매처 통계 비중을 모사한 사전 데이터베이스
if "survey_db" not in st.session_state:
    st.session_state.survey_db = pd.DataFrame([
        {"age": "20대", "freq": "자주 간다", "seat": "VIP 좌석", "spend": 160, "sat": 5, "genre": "K-POP / 아이돌", "with_who": "친구 / 동료"},
        {"age": "20대", "freq": "가끔 간다", "seat": "중간 좌석", "spend": 95, "sat": 4, "genre": "밴드 / 록 / 인디", "with_who": "연인"},
        {"age": "10대", "freq": "가끔 간다", "seat": "저가 좌석", "spend": 45, "sat": 3, "genre": "K-POP / 아이돌", "with_who": "혼자(혼콘)"},
        {"age": "30대 이상", "freq": "자주 간다", "seat": "VIP 좌석", "spend": 250, "sat": 5, "genre": "뮤지컬 / 극장 연극", "with_who": "가족"},
        {"age": "20대", "freq": "자주 간다", "seat": "VIP 좌석", "spend": 190, "sat": 5, "genre": "EDM / 대형 페스티벌", "with_who": "친구 / 동료"},
        {"age": "30대 이상", "freq": "가끔 간다", "seat": "중간 좌석", "spend": 120, "sat": 4, "genre": "클래식 / 오케스트라", "with_who": "연인"},
        {"age": "10대", "freq": "자주 간다", "seat": "중간 좌석", "spend": 85, "sat": 5, "genre": "밴드 / 록 / 인디", "with_who": "친구 / 동료"},
        {"age": "30대 이상", "freq": "가끔 간다", "seat": "VIP 좌석", "spend": 180, "sat": 4, "genre": "해외 아티스트 내한", "with_who": "연인"},
        {"age": "20대", "freq": "가끔 간다", "seat": "저가 좌석", "spend": 75, "sat": 4, "genre": "재즈 / 블루스 / 소울", "with_who": "혼자(혼콘)"},
        {"age": "20대", "freq": "자주 간다", "seat": "중간 좌석", "spend": 110, "sat": 5, "genre": "힙합 / R&B", "with_who": "친구 / 동료"}
    ])

if "last_match" not in st.session_state:
    st.session_state.last_match = None


# ── 3. 헤더 영역 ─────────────────────────────────────────
st.markdown("""
<div style="background:#ffffff; border-bottom:1px solid #e2e8f0; padding:1rem 2rem; display:flex; justify-content:space-between; align-items:center; margin-bottom:2rem;">
  <span style="font-family:'IBM Plex Mono',monospace; font-size:1.2rem; font-weight:700; color:#6366f1;">
    CONCERT<span style="color:#10b981;">.</span>PLATFORMS<span style="color:#94a3b8; font-weight:300;">_MEGA</span>
  </span>
  <span style="font-family:'IBM Plex Mono',monospace; font-size:0.7rem; color:#64748b; letter-spacing:0.1em;">
    TICKET COMBINED DATA HUB · 2026
  </span>
</div>
""", unsafe_allow_html=True)


# ── 🔥 실시간 큐레이션 매칭 결과 출력창 ───────────────────────
if st.session_state.last_match:
    match_data = st.session_state.last_match
    st.markdown('<p class="section-lbl">🎯 SURV_RESULT MATCHING</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-ttl">당신의 라이프스타일에 <em>정밀 제안된</em> 맞춤 공연</p>', unsafe_allow_html=True)
    
    box_col1, box_col2 = st.columns([1, 1.8])
    with box_col1:
        st.image(match_data["img"], use_container_width=True, caption=f"Recommended Concept Space - {match_data['name']}")
        
    with box_col2:
        st.markdown(f"""
        <div class="receipt-box">
            <span style="background:#10b981; color:#fff; font-size:0.75rem; padding:3px 12px; border-radius:20px; font-weight:bold;">{match_data['tag']}</span>
            <h2 style="margin:12px 0 6px 0; color:#0f172a; font-size:2rem;">{match_data['name']}</h2>
            <p style="font-size:1.05rem; color:#059669; font-weight:700; margin-bottom:12px;">선택 장르: {match_data['user_genre']} | 예상 평균 티켓가: ${match_data['cost']}</p>
            <p style="font-size:0.95rem; color:#334155; line-height:1.6; margin-bottom:18px;">
                "{match_data['desc']}"<br><br>
                💡 <b>시스템 코멘트:</b> 선택하신 장르 풀 안에서 유저님이 제안한 최대 지출 예산 한도인 <b>${match_data['user_budget']}</b> 가치에 매칭되는 가장 흥행 평점이 높은 아티스트를 종합 티켓 플랫폼에서 연동하여 빌드했습니다.
            </p>
            <a href="{match_data['url']}" target="_blank" class="ticket-btn" style="background-color:#10b981; padding:0.6rem 1.4rem; font-size:0.95rem;">🎟️ 연동된 공식 예매처에서 예매하기</a>
        </div>
        """, unsafe_allow_html=True)
        if st.button("❌ 추천 창 닫고 대시보드 보기"):
            st.session_state.last_match = None
            st.rerun()
    st.divider()


# ── 탭 레이아웃 구성 ──────────────────────────────────────────
tab1, tab2 = st.tabs(["📝 8대 장르 큐레이션 및 통계", "✨ 전체 확장 아티스트 도감"])

with tab1:
    col_input, col_recent = st.columns([1.2, 1], gap="large")

    with col_input:
        st.markdown('<p class="section-lbl">01 — MULTI-GENRE SURVEY</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-ttl">관객 <em>통합 장르</em> 라이프스타일 조사</p>', unsafe_allow_html=True)
        
        with st.form(key="mega_survey_form"):
            st.markdown("""
            <div class="survey-header">
                <span style="color:#6366f1; font-weight:700; font-size:0.9rem;">🔔 장르 다각화 업데이트</span>
                <p style="font-size:0.85rem; color:#475569; margin-top:4px;">예매처 실시간 인기 순위에 연동된 8가지 세분화 장르를 선택해 보세요.</p>
            </div>
            """, unsafe_allow_html=True)
            
            q1 = st.segmented_control("Q1. 연령대", ["10대", "20대", "30대 이상"], default="20대")
            q2 = st.selectbox("Q2. 평소 공연 관람 빈도", ["자주 간다", "가끔 간다", "거의 안 간다"])
            q3 = st.radio("Q3. 주로 예매하는 티켓 구역", ["VIP 좌석", "중간 좌석", "저가 좌석"], horizontal=True)
            q4 = st.slider("Q4. 콘서트 1회당 내 티켓 예산 한도 ($)", 30, 300, 150, step=5)
            q5 = st.select_slider("Q5. 최근 직관한 공연의 전반적인 만족도", options=[1, 2, 3, 4, 5], value=4)
            
            # [확장] 8대 장르 선택창
            q6 = st.selectbox("Q6. 가장 선호하는 음악 및 콘서트 장르는?", list(recommend_pool.keys()))
            q7 = st.radio("Q7. 콘서트는 주로 누구와 함께 가시나요?", ["혼자(혼콘)", "친구 / 동료", "연인", "가족"], horizontal=True)
            
            st.write("")
            submit = st.form_submit_button("🚀 설문 제출 및 맞춤 아티스트 결과 도출")
            
            if submit:
                new_row = pd.DataFrame([{"age": q1, "freq": q2, "seat": q3, "spend": q4, "sat": q5, "genre": q6, "with_who": q7}])
                st.session_state.survey_db = pd.concat([st.session_state.survey_db, new_row], ignore_index=True)
                
                # 정밀 필터링 로직: 선택한 장르 풀 안에서 사용자의 예산(q4) 이하인 최고의 아티스트 매칭
                pool = recommend_pool.get(q6, [])
                best_match = pool[0] # 기본값 예외 처리
                
                # 예산 이하인 아티스트 탐색
                for art in pool:
                    if art["cost"] <= q4:
                        best_match = art
                        break
                        
                best_match["user_genre"] = q6
                best_match["user_budget"] = q4
                st.session_state.last_match = best_match
                
                st.toast("통계 반영 및 맞춤 공연 매칭 완료!", icon="🎯")
                st.rerun()

    with col_recent:
        st.markdown('<p class="section-lbl">02 — INTERNET REAL LOGS</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-ttl">관객 <em>통합 플랫폼</em> 실시간 응답 피드</p>', unsafe_allow_html=True)
        
        data_log = st.session_state.survey_db.iloc[::-1].copy()
        data_log.columns = ["연령대", "빈도", "좌석", "지출($)", "만족도", "선호장르", "동행인"]
        st.dataframe(data_log, use_container_width=True, height=520)

    # ── 3. 대시보드 시각화 ─────────────────────────────────
    st.divider()
    df = st.session_state.survey_db
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='custom-card'><strong>🎵 세분화된 8대 장르 선호 비율</strong>", unsafe_allow_html=True)
        genre_val = df["genre"].value_counts()
        fig1 = go.Figure(go.Pie(labels=genre_val.index, values=genre_val.values, hole=0.4, 
                                marker=dict(colors=["#6366f1", "#10b981", "#f5a623", "#ec4899", "#8b5cf6", "#3b82f6", "#ef4444", "#64748b"])))
        fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#1e293b"), height=260)
        st.plotly_chart(fig1, use_container_width=True, key="mega_genre")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='custom-card'><strong>📊 관객 평균 지출 여력 트렌드 ($)</strong>", unsafe_allow_html=True)
        fig2 = go.Figure(go.Histogram(x=df["spend"], nbinsx=10, marker=dict(color="#6366f1", cornerradius=4)))
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#1e293b"), height=260)
        fig2.update_xaxes(gridcolor="#e2e8f0", zeroline=False)
        fig2.update_yaxes(gridcolor="#e2e8f0", zeroline=False)
        st.plotly_chart(fig2, use_container_width=True, key="mega_spend")
        st.markdown("</div>", unsafe_allow_html=True)


with tab2:
    # ── ✨ [신규 추가] 전체 확장 아티스트 도감 둘러보기 ────────────────────
    st.markdown('<p class="section-lbl">04 — ENCYCLOPEDIA</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-ttl">전체 장르별 <em>라인업 및 통합 예매처</em> 리스트</p>', unsafe_allow_html=True)
    st.write("본 플랫폼에 등록된 주요 티켓 사이트 연동 아티스트 도감입니다. 장르를 선택해 상세 정보를 탐색하세요.")
    
    selected_explore_genre = st.selectbox("둘러볼 장르 카테고리 선택", list(recommend_pool.keys()), key="explore_genre")
    
    explore_pool = recommend_pool[selected_explore_genre]
    
    # 2열 카드로 전체 풀 시각화 제공
    exp_col1, exp_col2 = st.columns(2, gap="large")
    
    with exp_col1:
        if len(explore_pool) > 0:
            item = explore_pool[0]
            st.image(item["img"], use_container_width=True)
            st.markdown(f"""
            <div class="custom-card">
                <span style="background:#6366f1; color:#fff; font-size:0.75rem; padding:3px 10px; border-radius:20px; font-weight:bold;">{item['tag']}</span>
                <h3 style="margin:8px 0 4px 0; color:#0f172a;">{item['name']}</h3>
                <p style="font-size:0.85rem; color:#6366f1; font-weight:700; margin-bottom:8px;">평균가 기준: ${item['cost']}</p>
                <p style="font-size:0.9rem; color:#475569; line-height:1.5;">{item['desc']}</p>
                <a href="{item['url']}" target="_blank" class="ticket-btn">🎟️ 예매 사이트 연결</a>
            </div>
            """, unsafe_allow_html=True)
            
    with exp_col2:
        if len(explore_pool) > 1:
            item = explore_pool[1]
            st.image(item["img"], use_container_width=True)
            st.markdown(f"""
            <div class="custom-card">
                <span style="background:#10b981; color:#fff; font-size:0.75rem; padding:3px 10px; border-radius:20px; font-weight:bold;">{item['tag']}</span>
                <h3 style="margin:8px 0 4px 0; color:#0f172a;">{item['name']}</h3>
                <p style="font-size:0.85rem; color:#10b981; font-weight:700; margin-bottom:8px;">평균가 기준: ${item['cost']}</p>
                <p style="font-size:0.9rem; color:#475569; line-height:1.5;">{item['desc']}</p>
                <a href="{item['url']}" target="_blank" class="ticket-btn">🎟️ 예매 사이트 연결</a>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("💡 해당 장르의 프리미엄 스페셜 단독 공연 라인업이 추가 준비 중입니다.")
