"""담양 리트릿 - 한옥 다방 Aesthetic"""

import streamlit as st

st.set_page_config(
    page_title="담양 리트릿",
    page_icon="🎋",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 한옥 다방 Design System
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Noto+Sans+KR:wght@300;400;500;600&display=swap');

:root {
    --hanji: #FDF8F3;
    --wood: #5D4037;
    --wood-light: #8B6914;
    --bamboo: #4A6741;
    --bamboo-light: #7A9E7E;
    --sienna: #C17F59;
    --cream: #F5EDE4;
    --ink: #2C2416;
    --ink-light: #6B5D4D;
}

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
    background: var(--hanji) !important;
}

.stApp {
    background:
        url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%' height='100%' filter='url(%23noise)'/%3E%3C/svg%3E"),
        linear-gradient(180deg, var(--hanji) 0%, var(--cream) 100%);
    background-blend-mode: overlay;
}

.block-container {
    padding: 1.5rem 1.25rem !important;
    max-width: 100% !important;
}

/* Hide default Streamlit elements */
#MainMenu, footer, header {visibility: hidden;}
.stDeployButton {display: none;}

/* Main Header */
.retreat-header {
    text-align: center;
    padding: 1rem 0 0.5rem;
    position: relative;
}

.retreat-header::before {
    content: "◇";
    display: block;
    color: var(--bamboo-light);
    font-size: 0.8rem;
    letter-spacing: 1rem;
    margin-bottom: 0.5rem;
    opacity: 0.6;
}

.retreat-title {
    font-family: 'Gowun Batang', serif;
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--wood);
    margin: 0;
    letter-spacing: -0.02em;
}

.retreat-subtitle {
    font-size: 0.8rem;
    color: var(--ink-light);
    margin-top: 0.25rem;
    font-weight: 300;
}

/* Base Card - Accommodation */
.base-card {
    background: linear-gradient(135deg, #FFF9F0 0%, #FDF3E7 100%);
    border: 1px solid var(--sienna);
    border-radius: 16px;
    padding: 1.25rem;
    margin: 1.25rem 0;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(93, 64, 55, 0.08);
}

.base-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--bamboo) 0%, var(--bamboo-light) 50%, var(--bamboo) 100%);
}

.base-label {
    display: inline-block;
    background: var(--bamboo);
    color: white;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.25rem 0.6rem;
    border-radius: 20px;
    letter-spacing: 0.05em;
    margin-bottom: 0.75rem;
}

.base-name {
    font-family: 'Gowun Batang', serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--wood);
    margin: 0 0 0.5rem;
}

.base-info {
    font-size: 0.8rem;
    color: var(--ink-light);
    line-height: 1.6;
}

.base-info span {
    display: block;
}

/* Schedule Strip */
.schedule-strip {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--cream);
    border-radius: 12px;
    padding: 0.875rem 1rem;
    margin-bottom: 1.25rem;
    border: 1px solid rgba(93, 64, 55, 0.1);
}

.schedule-icon {
    font-size: 1.1rem;
}

.schedule-flow {
    font-size: 0.8rem;
    color: var(--ink);
    font-weight: 400;
}

.schedule-flow strong {
    color: var(--wood);
    font-weight: 600;
}

/* Stats Bar */
.stats-bar {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.5rem;
    margin: 1rem 0;
}

.stat-pill {
    text-align: center;
    padding: 0.75rem 0.25rem;
    background: white;
    border-radius: 12px;
    border: 1px solid rgba(93, 64, 55, 0.1);
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}

.stat-value {
    font-family: 'Gowun Batang', serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--wood);
}

.stat-label {
    font-size: 0.8rem;
    color: var(--ink-light);
    margin-top: 0.15rem;
    font-weight: 500;
}

/* Action Buttons */
.stButton > button {
    background: var(--wood) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.875rem 1.5rem !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 12px rgba(93, 64, 55, 0.2) !important;
}

.stButton > button:hover {
    background: var(--ink) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 16px rgba(93, 64, 55, 0.25) !important;
}

.stButton > button[kind="secondary"] {
    background: white !important;
    color: var(--wood) !important;
    border: 1.5px solid var(--wood) !important;
    box-shadow: none !important;
}

.stButton > button[kind="secondary"]:hover {
    background: var(--cream) !important;
}

/* Section Headers */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 1.5rem 0 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--cream);
}

.section-icon {
    font-size: 1.1rem;
}

.section-title {
    font-family: 'Gowun Batang', serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--wood);
    margin: 0;
}

.section-hint {
    font-size: 0.8rem;
    color: var(--bamboo);
    background: rgba(74, 103, 65, 0.1);
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
    margin-left: auto;
}

/* Venue Cards */
.venue-card {
    background: white;
    border-radius: 14px;
    padding: 1rem;
    margin-bottom: 0.75rem;
    border: 1px solid rgba(93, 64, 55, 0.08);
    box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    transition: all 0.2s ease;
}

.venue-card:hover {
    border-color: var(--sienna);
    box-shadow: 0 4px 16px rgba(193, 127, 89, 0.12);
}

.venue-name {
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--ink);
    margin-bottom: 0.25rem;
}

.venue-detail {
    font-size: 0.8rem;
    color: var(--ink-light);
    line-height: 1.5;
}

.venue-tag {
    display: inline-block;
    font-size: 0.75rem;
    color: var(--bamboo);
    background: rgba(74, 103, 65, 0.08);
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
    margin-top: 0.35rem;
}

.venue-card {
    position: relative;
}

.venue-link {
    position: absolute;
    top: 0.75rem;
    right: 0.75rem;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    background: var(--cream);
    color: var(--wood);
    border: 1px solid var(--sienna);
    border-radius: 8px;
    text-decoration: none;
    font-size: 1rem;
    transition: all 0.2s ease;
}

.venue-link:hover {
    background: var(--sienna);
    color: white;
}

/* Link Buttons */
.stLinkButton > a {
    background: var(--cream) !important;
    color: var(--wood) !important;
    border: 1px solid var(--sienna) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}

/* Dividers */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--sienna), transparent);
    margin: 1.25rem 0;
    opacity: 0.3;
}

/* Caption styling */
.stCaption {
    color: var(--ink-light) !important;
}

/* Mobile Responsive */
@media (max-width: 600px) {
    .stats-bar {
        grid-template-columns: repeat(2, 1fr);
    }
    .stat-pill {
        padding: 0.6rem 0.5rem;
    }
    .retreat-title {
        font-size: 1.5rem;
    }
    .stLinkButton > a {
        min-height: 44px;
        padding: 0.5rem 1rem !important;
    }
}

/* Footer */
.footer-note {
    text-align: center;
    font-size: 0.7rem;
    color: var(--ink-light);
    margin-top: 2rem;
    padding: 1rem;
    opacity: 0.7;
}

.footer-note::before {
    content: "─ ◇ ─";
    display: block;
    margin-bottom: 0.5rem;
    letter-spacing: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="retreat-header">
    <h1 class="retreat-title">🎋 담양 리트릿</h1>
    <p class="retreat-subtitle">2026. 02. 13 — 14 · 4인 여행</p>
</div>
""", unsafe_allow_html=True)

# Base Accommodation Card
st.markdown("""
<div class="base-card">
    <span class="base-label">🏡 BASE CAMP</span>
    <h2 class="base-name">담양힐링파크 새연리조트</h2>
    <div class="base-info">
        <span>📍 봉산면 탄금길 9-26</span>
        <span>🚗 이하 모든 거리는 숙소 기준</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Schedule Strip
st.markdown("""
<div class="schedule-strip">
    <span class="schedule-icon">🗓</span>
    <span class="schedule-flow">
        <strong>11시</strong> 체크아웃 → <strong>점심</strong> → <strong>카페</strong> → <strong>소품샵</strong>
    </span>
</div>
""", unsafe_allow_html=True)

# Load data
from utils.data_loader import get_venues_df

df = get_venues_df()
total = len(df)
restaurants = len(df[df['category'] == 'restaurant'])
cafes = len(df[df['category'] == 'cafe'])
activities = len(df[df['category'] == 'activity'])

# Stats Bar
st.markdown(f"""
<div class="stats-bar">
    <div class="stat-pill">
        <div class="stat-value">{total}</div>
        <div class="stat-label">전체</div>
    </div>
    <div class="stat-pill">
        <div class="stat-value">{restaurants}</div>
        <div class="stat-label">🍚 식당</div>
    </div>
    <div class="stat-pill">
        <div class="stat-value">{cafes}</div>
        <div class="stat-label">☕ 카페</div>
    </div>
    <div class="stat-pill">
        <div class="stat-value">{activities}</div>
        <div class="stat-label">🎨 샵</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation
col1, col2 = st.columns(2)
with col1:
    if st.button("🗺️ 지도", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Map.py")
with col2:
    if st.button("📋 목록", use_container_width=True, type="secondary"):
        st.switch_page("pages/2_Places.py")

st.markdown("---")

# Lunch Section
st.markdown("""
<div class="section-header">
    <span class="section-icon">🍚</span>
    <h3 class="section-title">점심 추천</h3>
    <span class="section-hint">중식 제외</span>
</div>
""", unsafe_allow_html=True)

restaurant_df = df[df["category"] == "restaurant"]
restaurant_df = restaurant_df[~restaurant_df["subcategory"].isin(["중식"])]

for _, row in restaurant_df.iterrows():
    hours_text = f" · {row['hours']}" if row.get('hours') else ""
    note_tag = f'<span class="venue-tag">💡 {row["note"]}</span>' if row.get('note') and str(row.get('note')) != 'nan' else ""
    link_html = f'<a href="{row["url"]}" target="_blank" class="venue-link">→</a>' if row['url'] else ""

    st.markdown(f"""
    <div class="venue-card">
        {link_html}
        <div class="venue-name">{row['name']}</div>
        <div class="venue-detail">{row['feature']}{hours_text}</div>
        {note_tag}
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Cafe Section
st.markdown("""
<div class="section-header">
    <span class="section-icon">☕</span>
    <h3 class="section-title">카페 추천</h3>
</div>
""", unsafe_allow_html=True)

cafe_df = df[df["category"] == "cafe"].head(6)
for _, row in cafe_df.iterrows():
    note_tag = f'<span class="venue-tag">💡 {row["note"]}</span>' if row.get('note') and str(row.get('note')) != 'nan' else ""
    link_html = f'<a href="{row["url"]}" target="_blank" class="venue-link">→</a>' if row['url'] else ""

    st.markdown(f"""
    <div class="venue-card">
        {link_html}
        <div class="venue-name">{row['name']}</div>
        <div class="venue-detail">{row['feature']}</div>
        {note_tag}
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Shop Section
st.markdown("""
<div class="section-header">
    <span class="section-icon">🎨</span>
    <h3 class="section-title">소품샵</h3>
    <span class="section-hint">읍내 집중!</span>
</div>
""", unsafe_allow_html=True)

activity_df = df[df["category"] == "activity"]
for _, row in activity_df.iterrows():
    link_html = f'<a href="{row["url"]}" target="_blank" class="venue-link">→</a>' if row['url'] else ""

    st.markdown(f"""
    <div class="venue-card">
        {link_html}
        <div class="venue-name">{row['name']}</div>
        <div class="venue-detail">{row['feature']}</div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer-note">
    담양 여행의 모든 순간이 특별하길
</div>
""", unsafe_allow_html=True)
