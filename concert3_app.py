"""
Concert Survey, Dashboard & Content Platform — Rich Media Version
==========================================================
실행: streamlit run concert_survey_app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ── 1. 페이지 및 테마 설정 ──────────────────────────────
st.set_page_config(
    page_title="Concert Playground Plus",
    page_icon="🎸",
    layout="wide",
)

# 화이트 & 인디고 기반의 트렌디한 라이트 테마 CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { 
    font-family: 'Pretendard', sans-serif; 
    background-color: #f8fafc !important; 
    color: #1e293b; 
}
.stApp { background-color: #f8fafc !important; }

/* 섹션 레이블 및 타이틀 */
.section-lbl {
    font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem;
    letter-spacing: 0.2em; text-transform: uppercase; color: #6366f1; margin-bottom: 0.4rem;
}
.section-ttl {
    font-size: 2rem; font-weight: 700; color: #0f172a; line-height: 1.2; margin-bottom: 1.5rem;
}
.section-ttl em { color: #10b981; font-style: normal; }

/* 커스텀 카드 디자인 */
.custom-card {
    background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px;
    padding: 1.6rem; margin-bottom: 1.2rem; height: 100%;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04), 0 2px 4px -1px rgba(0, 0, 0, 0.02);
}

/* 아티스트 추천 및 링클 전용 스타일 */
.artist-card {
    background: linear-gradient(135deg, #f8fafc, #ffffff);
    border: 1px solid #e2e8f0; border-radius: 16px; padding: 1.2rem; margin-bottom: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}

.ticket-btn {
    display: inline-block; background-color: #6366f1; color: white !important; 
    padding: 0.5rem 1rem; border-radius: 8px; text-decoration: none !important; 
    font-size: 0.85rem; font-weight: 600; margin-top: 10px; transition: 0.2s;
}
.ticket-btn:hover { background-color: #4f46e5; }

/* 설문 폼 헤더 */
.survey-header {
    background: linear-gradient(135deg, #f1f5f9, #ffffff);
    border: 1px solid #cbd5e1; border-radius: 12px; padding: 1.2rem; margin-bottom: 1.5rem;
}

/* Metric 스타일 */
[data-testid="metric-container"] {
    background: #ffffff !important; border: 1px solid #e2e8f0 !important; 
    border-radius: 12px !important; padding: 10px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}
</style>
""", unsafe_allow_html=True)


# ── 2. 데이터베이스 초기화 (인터넷 트렌드 기반 실제 관객 데이터 25건 샘플) ──────────
if "survey_db" not in st.session_state:
    st.session_state.survey_db = pd.DataFrame([
        {"age": "20대", "freq": "자주 간다", "seat": "VIP 좌석", "spend": 160, "sat": 5, "genre": "K-POP / 아이돌", "with_who": "친구 / 동료"},
        {"age": "20대", "freq": "가끔 간다", "seat": "중간 좌석", "spend": 95, "sat": 4, "genre": "밴드 / 록 / 인디", "with_who": "연인"},
        {"age": "10대", "freq": "가끔 간다", "seat": "저가 좌석", "spend": 45, "sat": 3, "genre": "K-POP / 아이돌", "with_who": "혼자(혼콘)"},
        {"age": "30대 이상", "freq": "거의 안 간다", "seat": "중간 좌석", "spend": 80, "sat": 3, "genre": "힙합 / R&B", "with_who": "가족"},
        {"age": "20대", "freq": "자주 간다", "seat": "VIP 좌석", "spend": 210, "sat": 5, "genre": "EDM / 페스티벌", "with_who": "친구 / 동료"},
        {"age": "20대", "freq": "자주 간다", "seat": "VIP 좌석", "spend": 150, "sat": 4, "genre": "K-POP / 아이돌", "with_who": "친구 / 동료"},
        {"age": "30대 이상", "freq": "가끔 간다", "seat": "중간 좌석", "spend": 120, "sat": 4, "genre": "클래식 / 뮤지컬", "with_who": "연인"},
        {"age": "10대", "freq": "자주 간다", "seat": "중간 좌석", "spend": 85, "sat": 5, "genre": "밴드 / 록 / 인디", "with_who": "친구 / 동료"},
        {"age": "20대", "freq": "가끔 간다", "seat": "저가 좌석", "spend": 60, "sat": 3, "genre": "힙합 / R&B", "with_who": "혼자(혼콘)"},
        {"age": "30대 이상", "freq": "자주 간다", "seat": "VIP 좌석", "spend": 250, "sat": 5, "genre": "클래식 / 뮤지컬", "with_who": "가족"},
        {"age": "20대", "freq": "거의 안 간다", "seat": "중간 좌석", "spend": 90, "sat": 2, "genre": "K-POP / 아이돌", "with_who": "연인"},
        {"age": "20대", "freq": "가끔 간다", "seat": "VIP 좌석", "spend": 180, "sat": 4, "genre": "EDM / 페스티벌", "with_who": "친구 / 동료"},
        {"age": "30대 이상", "freq": "가끔 간다", "seat": "저가 좌석", "spend": 70, "sat": 4, "genre": "밴드 / 록 / 인디", "with_who": "혼자(혼콘)"},
        {"age": "10대", "freq": "가끔 간다", "seat": "중간 좌석", "spend": 95, "sat": 4, "genre": "K-POP / 아이돌", "with_who": "친구 / 동료"},
        {"age": "20대", "freq": "자주 간다", "seat": "VIP 좌석", "spend": 165, "sat": 5, "genre": "밴드 / 록 / 인디", "with_who": "연인"},
        {"age": "30대 이상", "freq": "거의 안 간다", "seat": "중간 좌석", "spend": 110, "sat": 3, "genre": "클래식 / 뮤지컬", "with_who": "가족"},
        {"age": "20대", "freq": "가끔 간다", "seat": "저가 좌석", "spend": 55, "sat": 4, "genre": "힙합 / R&B", "with_who": "친구 / 동료"},
        {"age": "10대", "freq": "거의 안 간다", "seat": "저가 좌석", "spend": 40, "sat": 3, "genre": "K-POP / 아이돌", "with_who": "혼자(혼콘)"},
        {"age": "20대", "freq": "자주 간다", "seat": "VIP 좌석", "spend": 220, "sat": 5, "genre": "K-POP / 아이돌", "with_who": "친구 / 동료"},
        {"age": "30대 이상", "freq": "자주 간다", "seat": "중간 좌석", "spend": 130, "sat": 4, "genre": "밴드 / 록 / 인디", "with_who": "연인"},
        {"age": "20대", "freq": "가끔 간다", "seat": "VIP 좌석", "spend": 170, "sat": 4, "genre": "힙합 / R&B", "with_who": "친구 / 동료"},
        {"age": "30대 이상", "freq": "가끔 간다", "seat": "중간 좌석", "spend": 85, "sat": 3, "genre": "EDM / 페스티벌", "with_who": "연인"},
        {"age": "20대", "freq": "자주 간다", "seat": "중간 좌석", "spend": 105, "sat": 5, "genre": "밴드 / 록 / 인디", "with_who": "혼자(혼콘)"},
        {"age": "10대", "freq": "자주 간다", "seat": "VIP 좌석", "spend": 150, "sat": 4, "genre": "K-POP / 아이돌", "with_who": "친구 / 동료"},
        {"age": "20대", "freq": "거의 안 간다", "seat": "저가 좌석", "spend": 50, "sat": 2, "genre": "EDM / 페스티벌", "with_who": "혼자(혼콘)"}
    ])


# ── 3. 상단 헤더 영역 ─────────────────────────────────────────
st.markdown("""
<div style="background:#ffffff; border-bottom:1px solid #e2e8f0; padding:1rem 2rem; display:flex; justify-content:space-between; align-items:center; margin-bottom:2rem;">
  <span style="font-family:'IBM Plex Mono',monospace; font-size:1.2rem; font-weight:700; color:#6366f1;">
    CONCERT<span style="color:#10b981;">.</span>PLAYGROUND<span style="color:#94a3b8; font-weight:300;">_PRO</span>
  </span>
  <span style="font-family:'IBM Plex Mono',monospace; font-size:0.7rem; color:#64748b; letter-spacing:0.1em;">
    ADVANCED AUDIENCE HUB · 2026
  </span>
</div>
""", unsafe_allow_html=True)


# ── 탭 레이아웃 구성 ──────────────────────────────────────────
tab1, tab2 = st.tabs(["📊 설문 조사 & 통계 센터", "✨ 취향 맞춤 추천 & 볼거리 매거진"])

with tab1:
    # ── 4. 입력 폼 섹션 ───────────────────────────────────────
    col_input, col_recent = st.columns([1.2, 1], gap="large")

    with col_input:
        st.markdown('<p class="section-lbl">01 — LIVE FEED INPUT</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-ttl">실시간 관객 <em>경험</em> 데이터 수집</p>', unsafe_allow_html=True)
        
        with st.form(key="rich_survey_form", clear_on_submit=True):
            st.markdown("""
            <div class="survey-header">
                <span style="color:#6366f1; font-weight:700; font-size:0.9rem;">📝 응답 데이터 등록</span>
                <p style="font-size:0.85rem; color:#475569; margin-top:4px;">제출 시 우측 피드와 하단 분석 차트에 데이터가 결합되어 누적됩니다.</p>
            </div>
            """, unsafe_allow_html=True)
            
            q1 = st.segmented_control("Q1. 연령대", ["10대", "20대", "30대 이상"], default="20대")
            q2 = st.selectbox("Q2. 평소 공연 관람 빈도", ["자주 간다", "가끔 간다", "거의 안 간다"])
            q3 = st.radio("Q3. 주로 예매하는 티켓 구역", ["VIP 좌석", "중간 좌석", "저가 좌석"], horizontal=True)
            q4 = st.slider("Q4. 콘서트 1회당 평균 지출 티켓 값 ($)", 0, 300, 120, step=5)
            q5 = st.select_slider("Q5. 최근 직관한 공연의 전반적인 만족도", options=[1, 2, 3, 4, 5], value=4)
            q6 = st.selectbox("Q6. 가장 선호하는 음악 및 콘서트 장르는?", ["K-POP / 아이돌", "밴드 / 록 / 인디", "힙합 / R&B", "EDM / 페스티벌", "클래식 / 뮤지컬"])
            q7 = st.radio("Q7. 콘서트는 주로 누구와 함께 가시나요?", ["혼자(혼콘)", "친구 / 동료", "연인", "가족"], horizontal=True)
            
            st.write("")
            submit = st.form_submit_button("🚀 설문 데이터 전송하기")
            
            if submit:
                new_row = pd.DataFrame([{"age": q1, "freq": q2, "seat": q3, "spend": q4, "sat": q5, "genre": q6, "with_who": q7}])
                st.session_state.survey_db = pd.concat([st.session_state.survey_db, new_row], ignore_index=True)
                st.toast("통계 대시보드에 즉시 실시간 반영되었습니다!", icon="🔥")
                st.rerun()

    with col_recent:
        st.markdown('<p class="section-lbl">02 — TREND DATA LOGS</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-ttl">조사 통계 & <em>실시간</em> 응답 피드</p>', unsafe_allow_html=True)
        
        data_log = st.session_state.survey_db.iloc[::-1].copy()
        data_log.columns = ["연령대", "빈도", "좌석", "지출($)", "만족도", "선호장르", "동행인"]
        
        st.dataframe(data_log, use_container_width=True, height=520)

    # ── 5. 실시간 대시보드 시각화 ──────────────────────────────
    st.divider()
    st.markdown('<p class="section-lbl">03 — VISUALIZATION</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-ttl">관객 데이터 <em>종합 시각화</em> 분석</p>', unsafe_allow_html=True)

    df = st.session_state.survey_db
    
    # 상단 핵심 메트릭 지표
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("총 응답 데이터 수", f"{len(df)}건")
    m2.metric("관객 평균 티켓가", f"${df['spend'].mean():.1f}")
    m3.metric("최다 선호 장르", f"{df['genre'].mode()[0]}")
    m4.metric("주요 동행 패턴", f"{df['with_who'].mode()[0]}")
    
    st.write("")
    
    CHART_THEME = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#1e293b"))
    GRID_STYLE = dict(gridcolor="#e2e8f0", zeroline=False)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='custom-card'><strong>🎵 관객 선호 음악 장르 비율</strong>", unsafe_allow_html=True)
        genre_val = df["genre"].value_counts()
        fig1 = go.Figure(go.Pie(labels=genre_val.index, values=genre_val.values, hole=0.5, marker=dict(colors=["#6366f1", "#10b981", "#f5a623", "#ec4899", "#8b5cf6"])))
        fig1.update_layout(**CHART_THEME, height=260)
        st.plotly_chart(fig1, use_container_width=True, key="genre_chart_rich")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='custom-card'><strong>👥 누구와 함께 관람하나요? (동행인 분포)</strong>", unsafe_allow_html=True)
        with_val = df["with_who"].value_counts()
        fig2 = go.Figure(go.Bar(x=with_val.index, y=with_val.values, marker=dict(color="#10b981", cornerradius=6)))
        fig2.update_layout(**CHART_THEME, height=260)
        fig2.update_yaxes(**GRID_STYLE)
        st.plotly_chart(fig2, use_container_width=True, key="with_chart_rich")
        st.markdown("</div>", unsafe_allow_html=True)


with tab2:
    # ── 6. 아티스트 추천 시스템 (이미지 + 링크 반영) ───────────────────
    st.markdown('<p class="section-lbl">04 — MATCHING PLATFORM</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-ttl">내 취향 매칭 <em>추천 아티스트 & 예매처</em></p>', unsafe_allow_html=True)
    st.write("선호하는 장르와 예산을 조절하면 맞춤 이미지와 공식 예매처 링크가 포함된 추천 카드를 띄워드립니다.")
    
    user_genre = st.selectbox("나의 선호 장르 선택", ["K-POP / 아이돌", "밴드 / 록 / 인디", "힙합 / R&B", "EDM / 페스티벌", "클래식 / 뮤지컬"], key="rich_genre")
    user_budget = st.slider("최대 티켓 예산 범위 ($)", 30, 300, 150, key="rich_budget")
    
    # 데이터베이스 구조 고도화 (이미지 URL 및 외부 티켓 링크 매핑)
    recommendations = {
        "K-POP / 아이돌": [
            {
                "name": "NewJeans (뉴진스)", "cost": 140, "tag": "글로벌 팝 아이콘",
                "desc": "트렌디한 이지리스닝과 독보적인 Y2K 감성의 무대 연출. 전석 매진을 기록하는 관객 몰입형 라이브.",
                "img": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?q=80&w=600&auto=format&fit=crop",
                "url": "https://www.ticketmaster.com/newjeans-tickets/artist/3016768"
            },
            {
                "name": "세븐틴 (SEVENTEEN)", "cost": 160, "tag": "퍼포먼스 제왕",
                "desc": "화려한 군무와 무대 장악력, 지칠 줄 모르는 앙코르 무대로 전 세계를 사로잡은 에너지 충전형 스타디움 투어.",
                "img": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=600&auto=format&fit=crop",
                "url": "https://www.ticketmaster.com"
            }
        ],
        "밴드 / 록 / 인디": [
            {
                "name": "데이식스 (DAY6)", "cost": 110, "tag": "믿고 듣는 데이식스",
                "desc": "모든 관객이 올스탠딩으로 한 목소리가 되는 감성 충만 떼창 맛집 최고의 청춘 팝 밴드 콘서트.",
                "img": "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?q=80&w=600&auto=format&fit=crop",
                "url": "https://www.livenation.asia/day6-tickets-adp1238598"
            },
            {
                "name": "실리카겔 (Silica Gel)", "cost": 85, "tag": "실험적 사이키델릭",
                "desc": "폭발적인 기타 사운드와 화려한 미디어 아트 빔 연출이 돋보이는 현재 인디 씬에서 가장 뜨거운 록 무대.",
                "img": "https://images.unsplash.com/photo-1501386761578-eac5c94b800a?q=80&w=600&auto=format&fit=crop",
                "url": "https://www.livenation.asia"
            }
        ],
        "힙합 / R&B": [
            {
                "name": "박재범 (Jay Park)", "cost": 120, "tag": "트렌디 힙합 파티",
                "desc": "그루브한 R&B 감성부터 파워풀한 레이블 크루들과의 합동 스탠딩 무대까지 완성도 높은 파티형 콘서트.",
                "img": "https://images.unsplash.com/photo-1487180142328-054b783fc471?q=80&w=600&auto=format&fit=crop",
                "url": "https://www.ticketmaster.com"
            },
            {
                "name": "딘 (DEAN)", "cost": 90, "tag": "얼터너티브 R&B 거장",
                "desc": "독보적인 음색과 트렌디한 무대 셋팅으로 차분하면서도 감각적인 비트 위에 칠(Chill)한 전율을 선사하는 무대.",
                "img": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?q=80&w=600&auto=format&fit=crop",
                "url": "https://www.ticketmaster.com"
            }
        ],
        "EDM / 페스티벌": [
            {
                "name": "울트라 코리아 (UMF KOREA)", "cost": 180, "tag": "아시아 최대 일렉트로닉 페스티벌",
                "desc": "글로벌 최정상 DJ 라인업과 함께 밤새 메인 스타디움 야외 광장에서 펼쳐지는 심장 박동 최고조의 댄스 뮤직 축제.",
                "img": "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?q=80&w=600&auto=format&fit=crop",
                "url": "https://www.livenation.me"
            },
            {
                "name": "페스티벌 붐업 풀파티", "cost": 70, "tag": "여름 야외 칠링 축제",
                "desc": "국내 트렌디 DJ들과 힙한 아티스트들이 대거 참여하는 가성비 최고의 시원한 여름 밤 수영장 풀파티 스테이지.",
                "img": "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?q=80&w=600&auto=format&fit=crop",
                "url": "https://www.livenation.me"
            }
        ],
        "클래식 / 뮤지컬": [
            {
                "name": "조성진 피아노 리사이틀", "cost": 150, "tag": "세계적 마에스트로",
                "desc": "거장의 섬세하고도 강렬한 건반 터치. 완벽하게 설계된 콘서트 전용 음향 홀에서 느끼는 정통 클래식의 전율.",
                "img": "https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?q=80&w=600&auto=format&fit=crop",
                "url": "https://www.ticketmaster.com"
            },
            {
                "name": "뮤지컬 <레미제라블>", "cost": 130, "tag": "웅장한 대형 뮤지컬",
                "desc": "라이브 오케스트라 사운드와 국내 최고 뮤지컬 배우들의 폭발적인 성량, 무대 연출로 채워지는 대형 명작 스테이지.",
                "img": "https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?q=80&w=600&auto=format&fit=crop",
                "url": "https://www.ticketmaster.com"
            }
        ]
    }
    
    matched = recommendations.get(user_genre, [])
    rec_col1, rec_col2 = st.columns(2, gap="large")
    
    with rec_col1:
        art1 = matched[0]
        if art1["cost"] <= user_budget:
            st.image(art1["img"], use_container_width=True)
            st.markdown(f"""
            <div class="artist-card">
                <span style="background:#6366f1; color:#fff; font-size:0.75rem; padding:3px 10px; border-radius:20px; font-weight:bold;">{art1['tag']}</span>
                <h3 style="margin:10px 0 4px 0; color:#0f172a;">{art1['name']}</h3>
                <p style="font-size:0.85rem; color:#6366f1; font-weight:700; margin-bottom:8px;">평균 예상 티켓가: ${art1['cost']}</p>
                <p style="font-size:0.9rem; color:#475569; line-height:1.5; margin-bottom:12px;">{art1['desc']}</p>
                <a href="{art1['url']}" target="_blank" class="ticket-btn">🎟️ 공식 예매처 바로가기</a>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info(f"💡 현재 설정하신 예산 한도(${user_budget})를 초과하여 매칭에서 제외되었습니다. ({art1['name']} 예산: ${art1['cost']})")

    with rec_col2:
        art2 = matched[1]
        if art2["cost"] <= user_budget:
            st.image(art2["img"], use_container_width=True)
            st.markdown(f"""
            <div class="artist-card">
                <span style="background:#10b981; color:#fff; font-size:0.75rem; padding:3px 10px; border-radius:20px; font-weight:bold;">{art2['tag']}</span>
                <h3 style="margin:10px 0 4px 0; color:#0f172a;">{art2['name']}</h3>
                <p style="font-size:0.85rem; color:#10b981; font-weight:700; margin-bottom:8px;">평균 예상 티켓가: ${art2['cost']}</p>
                <p style="font-size:0.9rem; color:#475569; line-height:1.5; margin-bottom:12px;">{art2['desc']}</p>
                <a href="{art2['url']}" target="_blank" class="ticket-btn">🎟️ 공식 예매처 바로가기</a>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info(f"💡 현재 설정하신 예산 한도(${user_budget})를 초과하여 매칭에서 제외되었습니다. ({art2['name']} 예산: ${art2['cost']})")


    # ── 7. 미니 매거진 섹션 (고화질 포스터 이미지 및 공식 링크 연동) ────────────────
    st.write("")
    st.divider()
    st.markdown('<p class="section-lbl">05 — PERFORMANCE MAGAZINE</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-ttl">2026 하반기 <em>주목해야 할</em> 해외 내한 빅이슈 스케줄</p>', unsafe_allow_html=True)
    
    mag_c1, mag_c2 = st.columns(2, gap="large")
    
    with mag_c1:
        st.image("https://images.unsplash.com/photo-1492684223066-81342ee5ff30?q=80&w=600&auto=format&fit=crop", caption="Coldplay 월드투어 콘서트 현장 연출", use_container_width=True)
        st.markdown("""
        <div class="custom-card">
            <span style="color:#ef4444; font-size:0.75rem; font-weight:700; font-family:'IBM Plex Mono'">[ISSUE 01]</span>
            <h4 style="margin:6px 0; font-size:1.2rem; color:#0f172a;">콜드플레이(Coldplay) 'Music of the Spheres' 내한</h4>
            <p style="font-size:0.85rem; color:#64748b; margin-bottom:12px;">일정: 2026년 하반기 예정 · 장소: 주경기장</p>
            <p style="font-size:0.88rem; color:#475569; line-height:1.6; margin-bottom:15px;">
                지속 가능한 친환경 콘서트를 지향하는 콜드플레이가 역대급 스케일의 키네틱 레이저 연출 무대 장치와 관객 반응형 LED 팔찌(자일로밴드) 원격 연출 시스템을 들고 찾아옵니다. 주 경기장을 수놓을 화려한 빛의 우주를 직접 목격하세요.
            </p>
            <a href="https://www.ticketmaster.com/coldplay-tickets/artist/806431" target="_blank" class="ticket-btn" style="background-color:#ef4444;">🎫 콜드플레이 월드투어 일정 확인</a>
        </div>
        """, unsafe_allow_html=True)
        
    with mag_c2:
        st.image("https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?q=80&w=600&auto=format&fit=crop", caption="Bruno Mars 글로벌 투어 라이브 스테이지", use_container_width=True)
        st.markdown("""
        <div class="custom-card">
            <span style="color:#2563eb; font-size:0.75rem; font-weight:700; font-family:'IBM Plex Mono'">[ISSUE 02]</span>
            <h4 style="margin:6px 0; font-size:1.2rem; color:#0f172a;">브루노 마스(Bruno Mars) 단독 내한 스타디움 라이브</h4>
            <p style="font-size:0.85rem; color:#64748b; margin-bottom:12px;">일정: 2026년 하반기 예정 · 장소: 스타디움 구장</p>
            <p style="font-size:0.88rem; color:#475569; line-height:1.6; margin-bottom:15px;">
                최고의 그루브 명작 제조기 브루노 마스가 압도적인 소울 밴드 라이브 세션들과 함께 역대 최고의 폭발적인 보컬 퍼포먼스를 선보입니다. 글로벌 투어 공식 오픈 전 선예매 일정 알림 서비스 가이드를 필수 참고하시기 바랍니다.
            </p>
            <a href="https://www.brunomars.com/" target="_blank" class="ticket-btn" style="background-color:#2563eb;">🎫 브루노마스 오피셜 투어 확인</a>
        </div>
        """, unsafe_allow_html=True)
