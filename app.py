"""Damyang Retreat Interactive Dashboard - Mobile-First Design."""

import streamlit as st

# Page configuration - mobile first
st.set_page_config(
    page_title="담양 리트릿",
    page_icon="🚗",
    layout="centered",  # Better for mobile
    initial_sidebar_state="collapsed",
)

# Mobile-friendly CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.block-container {
    padding: 1rem 1rem !important;
    max-width: 100% !important;
}

.main-title {
    font-size: 1.5rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 0.25rem;
}

.sub-title {
    font-size: 0.85rem;
    color: #6b7280;
    text-align: center;
    margin-bottom: 1rem;
}

.info-card {
    background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
}

.stat-row {
    display: flex;
    justify-content: space-around;
    gap: 0.5rem;
    margin: 1rem 0;
}

.stat-item {
    text-align: center;
    flex: 1;
    padding: 0.75rem 0.5rem;
    background: white;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.stat-number {
    font-size: 1.25rem;
    font-weight: 700;
    color: #1a1a1a;
}

.stat-label {
    font-size: 0.7rem;
    color: #6b7280;
}

.nav-btn {
    width: 100%;
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 12px;
    font-weight: 600;
}

.venue-item {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 0.75rem;
    margin-bottom: 0.5rem;
}

.venue-name {
    font-weight: 600;
    font-size: 0.95rem;
}

.venue-feature {
    color: #6b7280;
    font-size: 0.8rem;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-title">🚗 담양 리트릿</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">2026.02.13~14 · 4인</p>', unsafe_allow_html=True)

# Accommodation card - always prominent
st.markdown("""
<div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border-radius: 12px; padding: 1rem; margin-bottom: 1rem;
            border-left: 4px solid #f59e0b;">
    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
        <span style="font-size: 1.5rem;">🏡</span>
        <strong style="font-size: 1.1rem;">BASE: 담양힐링파크 새연리조트</strong>
    </div>
    <div style="color: #92400e; font-size: 0.85rem;">
        📍 봉산면 탄금길 9-26<br>
        🚗 모든 거리는 숙소 기준
    </div>
</div>
""", unsafe_allow_html=True)

# Schedule info
st.markdown("""
<div style="background: #f3f4f6; border-radius: 8px; padding: 0.75rem; margin-bottom: 1rem; font-size: 0.85rem;">
    <strong>🎯 일정:</strong> 체크아웃(11시) → 점심 → 카페 → 소품샵
</div>
""", unsafe_allow_html=True)

# Load data
from utils.data_loader import get_venues_df, CATEGORY_INFO

df = get_venues_df()

# Stats row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("전체", f"{len(df)}")
with col2:
    st.metric("🍚", f"{len(df[df['category'] == 'restaurant'])}")
with col3:
    st.metric("☕", f"{len(df[df['category'] == 'cafe'])}")
with col4:
    st.metric("🎨", f"{len(df[df['category'] == 'activity'])}")

st.markdown("---")

# Navigation buttons (top-down flow)
if st.button("🗺️ 지도 보기", use_container_width=True, type="primary"):
    st.switch_page("pages/1_Map.py")

if st.button("📋 전체 목록", use_container_width=True):
    st.switch_page("pages/2_Places.py")

st.markdown("---")

# Lunch recommendations (excluding Chinese food)
st.markdown("### 🍚 점심 추천")
st.caption("11시 이후 · 중식 제외")

restaurant_df = df[df["category"] == "restaurant"]
restaurant_df = restaurant_df[~restaurant_df["subcategory"].isin(["중식"])]

for _, row in restaurant_df.iterrows():
    with st.container():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**{row['name']}**")
            st.caption(f"{row['feature']} · {row.get('hours', '')}")
        with col2:
            if row['url']:
                st.link_button("→", row['url'], use_container_width=True)

st.markdown("---")

# Top cafes
st.markdown("### ☕ 추천 카페")

cafe_df = df[df["category"] == "cafe"].head(8)
for _, row in cafe_df.iterrows():
    with st.container():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**{row['name']}**")
            st.caption(f"{row['feature']}")
        with col2:
            if row['url']:
                st.link_button("→", row['url'], use_container_width=True)

st.markdown("---")

# Shops
st.markdown("### 🎨 소품샵")

activity_df = df[df["category"] == "activity"]
for _, row in activity_df.iterrows():
    with st.container():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**{row['name']}**")
            st.caption(f"{row['feature']}")
        with col2:
            if row['url']:
                st.link_button("→", row['url'], use_container_width=True)
