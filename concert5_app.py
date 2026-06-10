"""
Concert Playground Ultimate — Multi-Recommendation & Live Schedule Filter
========================================================================
실행: streamlit run concert_survey_app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ── 1. 페이지 및 라이트 테마 설정 ──────────────────────────────
st.set_page_config(
    page_title="Concert Playground Massive",
    page_icon="🎪",
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
    padding: 1.4rem; margin-bottom: 1.2rem; height: 100%;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
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
    font-size: 0.85rem; font-weight: 600; margin-top: 10px; text-align: center;
}
.ticket-btn:hover { background-color: #4f46e5; }

.survey-header {
    background: linear-gradient(135deg, #f1f5f9, #ffffff);
    border: 1px solid #cbd5e1; border-radius: 12px; padding: 1.2rem; margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)


# ── 2. [초대형 확장] 8대 장르 통합 글로벌 공연 라인업 풀 매핑 ───────────────────
recommend_pool = {
    "K-POP / 아이돌": [
        {"name": "NewJeans (뉴진스) 단독 콘서트", "cost": 130, "tag": "티켓링크 예매 1위", "desc": "트렌디한 Y2K 팝 멜로디와 독보적인 감성의 연출 스테이지.", "img": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?q=80&w=500", "url": "https://www.ticketlink.co.kr"},
        {"name": "세븐틴 (SEVENTEEN) 투어", "cost": 160, "tag": "인터파크 최다 매진", "desc": "잠실 주경기장을 뒤흔드는 압도적인 군무와 스태미나 페스티벌 무대.", "img": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=500", "url": "https://ticket.interpark.com"},
        {"name": "아이브 (IVE) 월드 투어", "cost": 120, "tag": "멜론티켓 단독", "desc": "화려하고 당당한 매력의 무대 연출과 관객 떼창이 폭발하는 팝 콘서트.", "img": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?q=80&w=500", "url": "https://ticket.melon.com"}
    ],
    "밴드 / 록 / 인디": [
        {"name": "실리카겔 (Silica Gel) 라이브", "cost": 80, "tag": "예스24 인디 1위", "desc": "폭발적인 기타 노이즈 사운드와 화려한 비주얼 미디어 아트의 전율.", "img": "https://images.unsplash.com/photo-1501386761578-eac5c94b800a?q=80&w=500", "url": "https://ticket.yes24.com"},
        {"name": "데이식스 (DAY6) 콘서트", "cost": 110, "tag": "멜론티켓 예매 폭주", "desc": "모든 관객이 하나 되어 노래하는 청춘을 대표하는 모던 밴드 사운드.", "img": "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?q=80&w=500", "url": "https://ticket.melon.com"},
        {"name": "루시 (LUCY) 청춘 단독공연", "cost": 90, "tag": "인터파크 인기작", "desc": "청량한 스트링 바이올린 사운드와 소년미 넘치는 경쾌한 에너지 밴드.", "img": "https://images.unsplash.com/photo-1511192336575-5a79af67a629?q=80&w=500", "url": "https://ticket.interpark.com"}
    ],
    "힙합 / R&B": [
        {"name": "박재범 (Jay Park) 힙합 파티", "cost": 120, "tag": "모어비전 크루 스페셜", "desc": "그루브 넘치는 R&B 보컬과 힙한 레이블 래퍼들의 화끈한 스탠딩 공연.", "img": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?q=80&w=500", "url": "https://ticket.melon.com"},
        {"name": "크러쉬 (Crush) 무드 콘서트", "cost": 105, "tag": "인터파크 소울 1위", "desc": "달콤하고 가슴 벅찬 음색으로 채워지는 로맨틱하고 칠(Chill)한 감성 라이브.", "img": "https://images.unsplash.com/photo-1487180142328-054b783fc471?q=80&w=500", "url": "https://ticket.interpark.com"},
        {"name": "딘 (DEAN) 얼터너티브 클럽", "cost": 95, "tag": "예스24 힙합", "desc": "감각적인 비트 위에 독보적인 소울을 얹은 몽환적인 R&B 밤샘 공연.", "img": "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?q=80&w=500", "url": "https://ticket.yes24.com"}
    ],
    "EDM / 대형 페스티벌": [
        {"name": "울트라 코리아 (UMF 2026)", "cost": 190, "tag": "글로벌 헤드라이너 최다", "desc": "세계 최정상 TOP DJ 라인업과 함께 즐기는 전자음악의 메카.", "img": "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?q=80&w=500", "url": "https://ticket.yes24.com"},
        {"name": "S2O KOREA (송크란 워터)", "cost": 140, "tag": "여름 초대형 워터뮤직", "desc": "강렬한 EDM 비트 속에 수만 리터의 물줄기가 쏟아지는 여름 필수 축제.", "img": "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?q=80&w=500", "url": "https://www.ticketlink.co.kr"}
    ],
    "뮤지컬 / 극장 연극": [
        {"name": "뮤지컬 <레미제라블>", "cost": 140, "tag": "초호화 블루스퀘어 라인업", "desc": "웅장한 오케스트라 선율과 명품 뮤지컬 배우들이 만들어내는 폭발적 성량.", "img": "https://images.unsplash.com/photo-1460723237483-7a6dc9d0b212?q=80&w=500", "url": "https://ticket.interpark.com"},
        {"name": "뮤지컬 <시카고> 내한", "cost": 110, "tag": "재즈 브로드웨이 팀", "desc": "매혹적인 앙상블 블랙 댄스와 라이브 재즈 오케스트라의 정통 무대.", "img": "https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?q=80&w=500", "url": "https://ticket.interpark.com"}
    ],
    "클래식 / 오케스트라": [
        {"name": "조성진 피아노 리사이틀", "cost": 150, "tag": "예술의전당 클래식 1위", "desc": "거장이 선사하는 완벽한 완급 조절과 전율 돋는 건반 사운드의 향연.", "img": "https://images.unsplash.com/photo-1552422535-c45813c61732?q=80&w=500", "url": "https://ticket.yes24.com"},
        {"name": "지브리 캔들라이트 콘서트", "cost": 70, "tag": "수천 개 촛불 로맨스", "desc": "은은한 촛불 조명 아래 펼쳐지는 현악 4중주 지브리 감성 영화 음악 메들리.", "img": "https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?q=80&w=500", "url": "https://ticket.interpark.com"}
    ],
    "재즈 / 블루스 / 소울": [
        {"name": "서울 재즈 페스티벌 2026", "cost": 180, "tag": "올림픽공원 잔디마당", "desc": "봄바람 부는 야외에서 와인과 함께 즐기는 최고 권위의 팝/재즈 야외 축제.", "img": "https://images.unsplash.com/photo-1484755560695-a4c748918c29?q=80&w=500", "url": "https://ticket.interpark.com"}
    ],
    "해외 아티스트 내한": [
        {"name": "콜드플레이 (Coldplay) 스타디움", "cost": 180, "tag": "역대급 불꽃 연출 레이저", "desc": "친환경 원격 반응형 LED 관객 팔찌가 만들어내는 환상적인 은하수 우주.", "img": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?q=80&w=500", "url": "https://ticket.interpark.com"},
        {"name": "브루노 마스 (Bruno Mars) 라이브", "cost": 220, "tag": "소울 펑크 완벽 스탠딩", "desc": "단 1초도 눈을 뗄 수 없는 완벽 보컬과 천재 펑크 브라스 브레이크 다운 무대.", "img": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?q=80&w=500", "url": "https://ticket.interpark.com"}
    ]
}

# 상시 오픈된 10개의 대표 아티스트 마스터 도감 리스트 (8개 이상 조건 충족)
master_encyclopedia = [
    {"name": "NewJeans", "genre": "K-POP / 아이돌", "cost": 130, "img": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?q=80&w=400", "url": "https://www.ticketlink.co.kr"},
    {"name": "세븐틴", "genre": "K-POP / 아이돌", "cost": 160, "img": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=400", "url": "https://ticket.interpark.com"},
    {"name": "실리카겔", "genre": "밴드 / 록 / 인디", "cost": 80, "img": "https://images.unsplash.com/photo-1501386761578-eac5c94b800a?q=80&w=400", "url": "https://ticket.yes24.com"},
    {"name": "데이식스", "genre": "밴드 / 록 / 인디", "cost": 110, "img": "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?q=80&w=400", "url": "https://ticket.melon.com"},
    {"name": "박재범", "genre": "힙합 / R&B", "cost": 120, "img": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?q=80&w=400", "url": "https://ticket.melon.com"},
    {"name": "울트라 코리아", "genre": "EDM / 대형 페스티벌", "cost": 190, "img": "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?q=80&w=400", "url": "https://ticket.yes24.com"},
    {"name": "뮤지컬 <레미제라블>", "genre": "뮤지컬 / 극장 연극", "cost": 140, "img": "https://images.unsplash.com/photo-1460723237483-7a6dc9d0b212?q=80&w=400", "url": "https://ticket.interpark.com"},
    {"name": "조성진 리사이틀", "genre": "클래식 / 오케스트라", "cost": 150, "img": "https://images.unsplash.com/photo-1552422535-c45813c61732?q=80&w=400", "url": "https://ticket.yes24.com"},
    {"name": "서울 재즈 페스티벌", "genre": "재즈 / 블루스 / 소울", "cost": 180, "img": "https://images.unsplash.com/photo-1484755560695-a4c748918c29?q=80&w=400", "url": "https://ticket.interpark.com"},
    {"name": "콜드플레이 내한", "genre": "해외 아티스트 내한", "cost": 180, "img": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?q=80&w=400", "url": "https://ticket.interpark.com"}
]

# 관객 통계 데이터베이스 기본 초기화
if "survey_db" not in st.session_state:
    st.session_state.survey_db = pd.DataFrame([
        {"age": "20대", "freq": "자주 간다", "seat": "VIP 좌석", "spend": 160, "sat": 5, "genre": "K-POP / 아이돌", "with_who": "친구 / 동료"},
        {"age": "20대", "freq": "가끔 간다", "seat": "중간 좌석", "spend": 95, "sat": 4, "genre": "밴드 / 록 / 인디", "with_who": "연인"},
        {"age": "30대 이상", "freq": "자주 간다", "seat": "VIP 좌석", "spend": 250, "sat": 5, "genre": "뮤지컬 / 극장 연극", "with_who": "가족"},
        {"age": "10대", "freq": "가끔 간다", "seat": "저가 좌석", "spend": 60, "sat": 4, "genre": "힙합 / R&B", "with_who": "혼자(혼콘)"}
    ])

# [필터 전용] 사용자가 설문을 마친 후 저장할 추천 리스트 (최소 3개 보장 목적)
if "last_triple_match" not in st.session_state:
    st.session_state.last_triple_match = None


# ── 3. 헤더 레이아웃 ─────────────────────────────────────────
st.markdown("""
<div style="background:#ffffff; border-bottom:1px solid #e2e8f0; padding:1rem 2rem; display:flex; justify-content:space-between; align-items:center; margin-bottom:2rem;">
  <span style="font-family:'IBM Plex Mono',monospace; font-size:1.2rem; font-weight:700; color:#6366f1;">
    CONCERT<span style="color:#10b981;">.</span>INTELLIGENT<span style="color:#94a3b8; font-weight:300;">_MAX</span>
  </span>
  <span style="font-family:'IBM Plex Mono',monospace; font-size:0.7rem; color:#64748b; letter-spacing:0.1em;">
    ULTIMATE SELECTION HUB · 2026
  </span>
</div>
""", unsafe_allow_html=True)


# ── 🔥 [1번 요구사항 반영] 설문조사 끝난 직후 3개 맞춤 공연 대형 매칭 창 ───────────────────
if st.session_state.last_triple_match:
    matches = st.session_state.last_triple_match
    st.markdown('<p class="section-lbl">🎯 SURV_RESULT TRIPLE MATCH</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-ttl">회원님의 라이프스타일 매칭 <em>추천 리스트 (Top 3)</em></p>', unsafe_allow_html=True)
    
    # 3개 추천 공연 카드 병렬 배치
    c3_1, c3_2, c3_3 = st.columns(3, gap="large")
    
    cols = [c3_1, c3_2, c3_3]
    for idx, item in enumerate(matches[:3]):
        with cols[idx]:
            st.image(item["img"], use_container_width=True)
            st.markdown(f"""
            <div class="receipt-box" style="height:280px; margin-bottom:0;">
                <span style="background:#10b981; color:#fff; font-size:0.72rem; padding:2px 8px; border-radius:20px; font-weight:bold;">✨ 추천 순위 0{idx+1}</span>
                <h3 style="margin:8px 0 4px 0; color:#0f172a; font-size:1.25rem;">{item['name']}</h3>
                <p style="font-size:0.85rem; color:#059669; font-weight:700; margin-bottom:6px;">예상 티켓가: ${item['cost']}</p>
                <p style="font-size:0.85rem; color:#475569; line-height:1.4; height:70px; overflow:hidden;">{item['desc']}</p>
                <a href="{item['url']}" target="_blank" class="ticket-btn" style="background-color:#10b981; font-size:0.8rem; width:100%;">🎟️ 공식 제휴처 예매하기</a>
            </div>
            """, unsafe_allow_html=True)
            
    st.write("")
    if st.button("❌ 맞춤 3가지 제안 확인 완료 (닫기)", use_container_width=True):
        st.session_state.last_triple_match = None
        st.rerun()
    st.divider()


# ── 4. 메인 탭 시스템 ──────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📝 큐레이션 및 관객 분석", "🔍 장르별 예정작 스케줄 구경", "✨ 마스터 아티스트 도감 (10대 명작)"])

with tab1:
    col_input, col_recent = st.columns([1.2, 1], gap="large")

    with col_input:
        st.markdown('<p class="section-lbl">01 — LIFESTYLE INQUIRY</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-ttl">관객 <em>맞춤 추천형</em> 설문조사</p>', unsafe_allow_html=True)
        
        with st.form(key="massive_survey_form"):
            st.markdown("""
            <div class="survey-header">
                <span style="color:#6366f1; font-weight:700; font-size:0.9rem;">🔔 실시간 완결 추천 가동 중</span>
                <p style="font-size:0.85rem; color:#475569; margin-top:4px;">작성을 마친 뒤 전송하면 최상단에 <b>3개의 추천 라인업</b>이 동시 출력됩니다.</p>
            </div>
            """, unsafe_allow_html=True)
            
            q1 = st.segmented_control("Q1. 연령대", ["10대", "20대", "30대 이상"], default="20대")
            q2 = st.selectbox("Q2. 평소 공연 관람 빈도", ["자주 간다", "가끔 간다", "거의 안 간다"])
            q3 = st.radio("Q3. 주로 예매하는 티켓 구역", ["VIP 좌석", "중간 좌석", "저가 좌석"], horizontal=True)
            q4 = st.slider("Q4. 콘서트 1회당 내 티켓 예산 한도 ($)", 30, 300, 160, step=5)
            q5 = st.select_slider("Q5. 최근 직관한 공연의 전반적인 만족도", options=[1, 2, 3, 4, 5], value=4)
            q6 = st.selectbox("Q6. 가장 선호하는 음악 및 콘서트 장르는?", list(recommend_pool.keys()))
            q7 = st.radio("Q7. 콘서트는 주로 누구와 함께 가시나요?", ["혼자(혼콘)", "친구 / 동료", "연인", "가족"], horizontal=True)
            
            st.write("")
            submit = st.form_submit_button("🚀 설문 제출 및 결과 인쇄하기")
            
            if submit:
                # 대시보드 누적
                new_row = pd.DataFrame([{"age": q1, "freq": q2, "seat": q3, "spend": q4, "sat": q5, "genre": q6, "with_who": q7}])
                st.session_state.survey_db = pd.concat([st.session_state.survey_db, new_row], ignore_index=True)
                
                # [3개 매칭 알고리즘 구현]
                # 해당 장르에서 아티스트 풀 로드
                selected_pool = recommend_pool.get(q6, [])
                
                # 만약 풀이 3개보다 작을 경우를 대비해, 타 장르 아티스트를 서브 백업으로 통합
                final_matches = []
                for art in selected_pool:
                    final_matches.append(art)
                
                # 혹시라도 예산 범위 내 다른 장르 베스트셀러를 엮어서라도 3개 세트 충족 보장
                if len(final_matches) < 3:
                    for ext_genre, ext_artists in recommend_pool.items():
                        if ext_genre != q6:
                            for art in ext_artists:
                                if art not in final_matches:
                                    final_matches.append(art)
                                if len(final_matches) >= 3:
                                    break
                        if len(final_matches) >= 3:
                            break
                            
                st.session_state.last_triple_match = final_matches[:3]
                st.toast("당신을 위한 3개의 공연 큐레이션이 빌드되었습니다!", icon="🎯")
                st.rerun()

    with col_recent:
        st.markdown('<p class="section-lbl">02 — LOG FEED</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-ttl">관객 <em>종합 수집</em> 데이터 실시간 로그 피드</p>', unsafe_allow_html=True)
        
        data_log = st.session_state.survey_db.iloc[::-1].copy()
        data_log.columns = ["연령대", "빈도", "좌석", "지출($)", "만족도", "선호장르", "동행인"]
        st.dataframe(data_log, use_container_width=True, height=520)

    # ── 대시보드 분석 그래프 ───────────────────────────────
    st.divider()
    df = st.session_state.survey_db
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='custom-card'><strong>🎵 세분화된 8대 장르 선호도 누적 통계</strong>", unsafe_allow_html=True)
        genre_val = df["genre"].value_counts()
        fig1 = go.Figure(go.Pie(labels=genre_val.index, values=genre_val.values, hole=0.4, marker=dict(colors=["#6366f1", "#10b981", "#f5a623", "#ec4899", "#8b5cf6"])))
        fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#1e293b"), height=250)
        st.plotly_chart(fig1, use_container_width=True, key="pie_chart")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='custom-card'><strong>👥 동행 패턴 통계 비중</strong>", unsafe_allow_html=True)
        with_val = df["with_who"].value_counts()
        fig2 = go.Figure(go.Bar(x=with_val.index, y=with_val.values, marker=dict(color="#10b981", cornerradius=5)))
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#1e293b"), height=250)
        st.plotly_chart(fig2, use_container_width=True, key="bar_chart")
        st.markdown("</div>", unsafe_allow_html=True)


with tab2:
    # ── 🌟 [3번 요구사항 반영] 장르별 실시간 오픈 예정인 공연 구경 창 ───────────────────
    st.markdown('<p class="section-lbl">03 — OPEN SCHEDULE LIVE WINDOW</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-ttl">실시간 카테고리별 <em>공연 예정작</em> 무한 구경 피드</p>', unsafe_allow_html=True)
    st.write("원하는 장르 카테고리를 필터링하면 국내외 티켓팅 플랫폼에 오픈 대기/예정인 실제 스타일의 콘서트 라인업 스케줄을 생생하게 탐색할 수 있습니다.")
    
    filter_genre = st.radio("구경할 장르 카테고리 탭 선택", list(recommend_pool.keys()), horizontal=True)
    
    st.write("")
    selected_scheduled_shows = recommend_pool.get(filter_genre, [])
    
    # 윈도우 스타일 형태로 포스터와 스케줄 렌더링
    grid_c = st.columns(len(selected_scheduled_shows))
    for idx, show in enumerate(selected_scheduled_shows):
        with grid_c[idx]:
            st.image(show["img"], use_container_width=True)
            st.markdown(f"""
            <div class="custom-card">
                <span style="background:#6366f1; color:white; font-size:0.7rem; padding:2px 8px; border-radius:4px; font-weight:700;">{show['tag']}</span>
                <h4 style="margin:8px 0 2px 0; font-size:1.1rem; color:#0f172a;">{show['name']}</h4>
                <p style="font-size:0.8rem; color:#64748b; font-weight:bold; margin-bottom:10px;">스케줄 등급가: ${show['cost']}</p>
                <p style="font-size:0.85rem; color:#475569; line-height:1.5; height:60px; overflow:hidden;">{show['desc']}</p>
                <a href="{show['url']}" target="_blank" class="ticket-btn" style="width:100%;">🎟️ 공연 예매/좌석 정보 구경</a>
            </div>
            """, unsafe_allow_html=True)


with tab3:
    # ── 🌟 [2번 요구사항 반영] 8개 이상의 다채로운 마스터 아티스트 도감 ───────────────────
    st.markdown('<p class="section-lbl">04 — MASTER ENCYCLOPEDIA</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-ttl">종합 플랫폼 등록 <em>마스터 아티스트 도감 (10대 명작)</em></p>', unsafe_allow_html=True)
    st.write("본 서비스 아카이브에 연동된 총 10팀의 국가대표 및 글로벌 최고 권위 아티스트 데이터 센터 리스트입니다.")
    
    # 5열 배치 구조로 10개 카드를 미려하게 바인딩
    row1_cols = st.columns(5, gap="medium")
    row2_cols = st.columns(5, gap="medium")
    
    all_ency_cols = row1_cols + row2_cols
    
    for idx, artist in enumerate(master_encyclopedia):
        with all_ency_cols[idx]:
            st.image(artist["img"], use_container_width=True)
            st.markdown(f"""
            <div class="custom-card" style="text-align:center; padding:1rem;">
                <p style="font-size:0.75rem; color:#6366f1; font-weight:bold; margin:0;">{artist['genre']}</p>
                <h4 style="margin:4px 0; font-size:1.2rem; color:#0f172a;">{artist['name']}</h4>
                <p style="font-size:0.8rem; color:#64748b; margin-bottom:8px;">평균가: ${artist['cost']}</p>
                <a href="{artist['url']}" target="_blank" style="font-size:0.75rem; padding:4px 10px; background:#f1f5f9; color:#475569 !important; border-radius:6px; text-decoration:none; display:inline-block; border:1px solid #cbd5e1;">🔍 아티스트 상세 프로필</a>
            </div>
            """, unsafe_allow_html=True)
