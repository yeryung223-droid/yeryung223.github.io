"""
Concert Survey & Real-time Dashboard — Streamlit App
======================================================
실행:
    pip install streamlit plotly pandas
    streamlit run concert_survey_app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ── 1. 페이지 및 테마 설정 ───────────────────────────────────
st.set_page_config(
    page_title="Concert Survey Center",
    page_icon="📊",
    layout="wide",
)

# 고급스러운 다크네이비/크림/포인트 네온 컬러 CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

html, body, [class*="css"] { font-family:'Lora',Georgia,serif; }
.stApp, .stMainBlockContainer { background:#07080a !important; color:#f0ece4; }

/* 섹션 타이틀 스타일 */
.section-lbl {
    font-family:'IBM Plex Mono',monospace; font-size:.65rem;
    letter-spacing:.3em; text-transform:uppercase; color:#e84545; margin-bottom:.3rem;
}
.section-ttl {
    font-size:2.2rem; font-weight:600; color:#f0ece4; line-height:1.1; margin-bottom:1.5rem;
}
.section-ttl em { color:#f5a623; font-style:normal; }

/* 카드 디자인 */
.custom-card {
    background:#0f1014; border:1px solid #1e1e26; border-radius:14px;
    padding:1.8rem; margin-bottom:1rem; height:100%;
}

/* 설문 폼 스타일 마크업 */
.survey-header {
    background: linear-gradient(135deg, #1e1212, #0f1014);
    border: 1px solid #3d1b1b; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem;
}

/* Metric 커스텀 */
[data-testid="metric-container"] {
    background:#0f1014 !important; border:1px solid #1e1e26 !important; border-radius:12px !important;
}
[data-testid="stMetricLabel"]  { color:#6b6878 !important; font-family:'IBM Plex Mono',monospace; }
[data-testid="stMetricValue"]  { color:#f0ece4 !important; }
</style>
""", unsafe_allow_html=True)


# ── 2. 가상 가상 데이터베이스 (Session State) 초기화 ───────────────
# 앱이 재실행되어도 사용자들이 제출한 데이터가 휘발되지 않고 누적되도록 합니다.
if "survey_db" not in st.session_state:
    # 대시보드가 처음부터 비어있지 않도록 기본 초기 데이터 5건을 심어둡니다.
    st.session_state.survey_db = pd.DataFrame([
        {"age": "20대", "freq": "자주 간다", "seat": "VIP 좌석", "spend": 150, "sat": 5},
        {"age": "20대", "freq": "가끔 간다", "seat": "중간 좌석", "spend": 90, "sat": 4},
        {"age": "10대", "freq": "가끔 간다", "seat": "저가 좌석", "spend": 40, "sat": 3},
        {"age": "30대 이상", "freq": "거의 안 간다", "seat": "중간 좌석", "spend": 75, "sat": 3},
        {"age": "30대 이상", "freq": "자주 간다", "seat": "VIP 좌석", "spend": 180, "sat": 5},
    ])


# ── 3. 헤더 영역 ─────────────────────────────────────────────
st.markdown("""
<div style="background:#0f1014; border:1px solid #1e1e26; border-radius:12px; padding:.9rem 1.8rem; display:flex; justify-content:between; align-items:center; margin-bottom:2rem;">
  <span style="font-family:'IBM Plex Mono',monospace; font-size:1.1rem; font-weight:700; color:#e84545; letter-spacing:.06em;">
    CONCERT<span style="color:#f0ece4;">.</span>SURVEY<span style="color:#6b6878; font-weight:300;">_CENTER</span>
  </span>
  <span style="font-family:'IBM Plex Mono',monospace; font-size:.65rem; letter-spacing:.2em; color:#6b6878;">
    LIVE AUDIENCE RESEARCH · 2026
  </span>
</div>
""", unsafe_allow_html=True)


# ── 4. 좌측: 설문조사 입력 폼 / 우측: 실시간 가이드 ──────────────────
col_form, col_guide = st.columns([1.4, 1], gap="large")

with col_form:
    st.markdown('<p class="section-lbl">PART 01 — INPUT</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-ttl">관객 <em>설문조사</em> 참여</p>', unsafe_allow_html=True)
    
    with st.form(key="concert_survey_form", clear_on_submit=True):
        st.markdown("""
        <div class="survey-header">
            <span style="color:#e84545; font-weight:bold; font-size:0.9rem;">Notice</span>
            <p style="font-size:0.85rem; color:#6b6878; margin:4px 0 0 0;">본 설문은 익명으로 진행되며, 제출 시 하단의 실시간 통계 대시보드 차트에 즉시 반영됩니다.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 문항 레이아웃
        q1 = st.radio("Q1. 연령대가 어떻게 되시나요?", ["10대", "20대", "30대 이상"])
        st.write("")
        q2 = st.selectbox("Q2. 평소 콘서트(라이브 공연)에 얼마나 자주 가시나요?", ["자주 간다", "가끔 간다", "거의 안 간다"])
        st.write("")
        q3 = st.radio("Q3. 가장 선호하거나 주로 예매하는 좌석 구역은 어디인가요?", ["VIP 좌석", "중간 좌석", "저가 좌석"])
        st.write("")
        q4 = st.slider("Q4. 콘서트 티켓 1매당 평균 지출 금액은 얼마인가요? (USD $)", min_value=10, max_value=300, value=100, step=5)
        st.write("")
        q5 = st.select_slider("Q5. 최근에 다녀온 콘서트의 전반적인 만족도는 어떠셨나요?", options=[1, 2, 3, 4, 5], value=4)
        
        st.write("")
        submit_button = st.form_submit_button(label="📊 설문 데이터 제출하기")
        
        if submit_button:
            # 새 응답 데이터를 데이터프레임 구조로 생성
            new_data = pd.DataFrame([{"age": q1, "freq": q2, "seat": q3, "spend": q4, "sat": q5}])
            # 기존 DB에 결합 및 인덱스 리셋
            st.session_state.survey_db = pd.concat([st.session_state.survey_db, new_data], ignore_index=True)
            st.success("설문이 성공적으로 임베디드 되었습니다! 아래 대시보드를 확인하세요.")
            st.rerun()

with col_guide:
    st.markdown('<p class="section-lbl">PART 02 — LIVE DATA LOG</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-ttl">최근 <em>제출된</em> 데이터</p>', unsafe_allow_html=True)
    
    # 세션 상태에 저장된 현재까지의 데이터 요약 표 보여주기
    current_df = st.session_state.survey_db
    
    st.markdown(f"**총 누적 응답수:** `{len(current_df)}건`")
    
    # 데이터 가독성을 높인 역순 테이블 (최신 응답이 위로 오게)
    display_df = current_df.iloc[::-1].copy()
    display_df.columns = ["연령대", "관람 빈도", "선호 좌석", "평균 지출($)", "만족도(5점)"]
    
    st.dataframe(
        display_df.style.background_gradient(subset=["만족도(5점)"], cmap="YlOrRd")
                       .background_gradient(subset=["평균 지출($)"], cmap="Blues"),
        use_container_width=True,
        height=400
    )


# ── 5. 하단: 실시간 통계 대시보드 영역 ──────────────────────────────
st.divider()
st.markdown('<p class="section-lbl">PART 03 — REAL-TIME DASHBOARD</p>', unsafe_allow_html=True)
st.markdown('<p class="section-ttl">설문 결과 <em>실시간 시각화</em> 분석</p>', unsafe_allow_html=True)

df_stats = st.session_state.survey_db

if not df_stats.empty:
    # ── 상단 주요 지표 요약 (Metrics)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="👥 총 설문 참여자", value=f"{len(df_stats)} 명")
    with m2:
        avg_spend = df_stats["spend"].mean()
        st.metric(label="💸 평균 티켓 지출액", value=f"${avg_spend:.1f}")
    with m3:
        avg_sat = df_stats["sat"].mean()
        st.metric(label="⭐ 평균 관람 만족도", value=f"{avg_sat:.2f} / 5.0")
    with m4:
        vip_ratio = (len(df_stats[df_stats["seat"] == "VIP 좌석"]) / len(df_stats)) * 100
        st.metric(label="💎 VIP 좌석 선호도", value=f"{vip_ratio:.1f} %")

    st.write("")

    # ── 차트 시각화 레이아웃 (2x2 구조)
    BG_COLOR = "#07080a"
    GRID_COLOR = "rgba(255,255,255,.06)"
    TEXT_STYLE = dict(color="rgba(240,236,228,.72)", family="IBM Plex Mono")
    
    ch_col1, ch_col2 = st.columns(2, gap="medium")
    
    # 차트 1: 좌석 선호도 비율 (파이 차트)
    with ch_col1:
        st.markdown("<div class='custom-card'><strong>🪑 구역별 좌석 선호 비중</strong>", unsafe_allow_html=True)
        seat_counts = df_stats["seat"].value_counts()
        fig_pie = go.Figure(go.Pie(
            labels=seat_counts.index, values=seat_counts.values, hole=0.5,
            marker=dict(colors=["#e84545", "#f5a623", "#3ecf8e"]),
            textinfo="percent+label"
        ))
        fig_pie.update_layout(
            paper_bgcolor=BG_COLOR, plot_bgcolor=BG_COLOR, font=TEXT_STYLE,
            margin=dict(l=20, r=20, t=30, b=20), showlegend=False, height=280
        )
        st.plotly_chart(fig_pie, use_container_width=True, key="live_pie")
        st.markdown("</div>", unsafe_allow_html=True)
        
    # 차트 2: 지출 금액 vs 만족도 관계 (산점도)
    with ch_col2:
        st.markdown("<div class='custom-card'><strong>📈 지출 금액과 만족도의 상관관계</strong>", unsafe_allow_html=True)
        fig_scatter = go.Figure(go.Scatter(
            x=df_stats["spend"], y=df_stats["sat"], mode="markers",
            marker=dict(size=14, color="#3ecf8e", line=dict(color="#fff", width=1)),
            hovertemplate="지출: $%{x}<br>만족도: %{y}점<extra></extra>"
        ))
        fig_scatter.update_layout(
            paper_bgcolor=BG_COLOR, plot_bgcolor=BG_COLOR, font=TEXT_STYLE,
            margin=dict(l=20, r=20, t=30, b=20), height=280
        )
        fig_scatter.update_xaxes(title="티켓 비용 ($)", gridcolor=GRID_COLOR, zeroline=False)
        fig_scatter.update_yaxes(title="만족도", gridcolor=GRID_COLOR, range=[0.5, 5.5], tickvals=[1,2,3,4,5])
        st.plotly_chart(fig_scatter, use_container_width=True, key="live_scatter")
        st.markdown("</div>", unsafe_allow_html=True)

    ch_col3, ch_col4 = st.columns(2, gap="medium")
    
    # 차트 3: 연령대별 평균 지출액 (바 차트)
    with ch_col3:
        st.markdown("<div class='custom-card'><strong>📊 연령대별 평균 지출 현황</strong>", unsafe_allow_html=True)
        age_spend = df_stats.groupby("age")["spend"].mean().reindex(["10대", "20대", "30대 이상"]).fillna(0)
        fig_bar = go.Figure(go.Bar(
            x=age_spend.index, y=age_spend.values,
            marker=dict(color="#f5a623", cornerradius=6),
            text=[f"${v:.0f}" for v in age_spend.values], textposition="outside"
        ))
        fig_bar.update_layout(
            paper_bgcolor=BG_COLOR, plot_bgcolor=BG_COLOR, font=TEXT_STYLE,
            margin=dict(l=20, r=20, t=40, b=20), height=280
        )
        fig_bar.update_yaxes(gridcolor=GRID_COLOR, zeroline=False)
        st.plotly_chart(fig_bar, use_container_width=True, key="live_bar_age")
        st.markdown("</div>", unsafe_allow_html=True)

    # 차트 4: 관람 빈도 현황 분포 (히스토그램형 바 차트)
    with ch_col4:
        st.markdown("<div class='custom-card'><strong>🏃 관람 빈도별 유저 분포</strong>", unsafe_allow_html=True)
        freq_counts = df_stats["freq"].value_counts().reindex(["자주 간다", "가끔 간다", "거의 안 간다"]).fillna(0)
        fig_freq = go.Figure(go.Bar(
            x=freq_counts.index, y=freq_counts.values,
            marker=dict(color="#e84545", cornerradius=6),
            text=[f"{int(v)}명" for v in freq_counts.values], textposition="outside"
        ))
        fig_freq.update_layout(
            paper_bgcolor=BG_COLOR, plot_bgcolor=BG_COLOR, font=TEXT_STYLE,
            margin=dict(l=20, r=20, t=40, b=20), height=280
        )
        fig_freq.update_yaxes(gridcolor=GRID_COLOR, zeroline=False)
        st.plotly_chart(fig_freq, use_container_width=True, key="live_bar_freq")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.warning("데이터베이스가 비어있습니다. 첫 설문을 작성해 주세요!")
