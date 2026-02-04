"""Interactive Map View - Mobile First."""

import streamlit as st
import folium
from streamlit_folium import st_folium

from utils.data_loader import (
    get_venues_df,
    get_accommodation,
    CATEGORY_INFO,
    get_category_color,
)

st.set_page_config(
    page_title="지도 - 담양 리트릿",
    page_icon="🗺️",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
.block-container { padding: 0.5rem 0.5rem !important; }
</style>
""", unsafe_allow_html=True)

# Back button
if st.button("← 홈으로"):
    st.switch_page("app.py")

st.markdown("## 🗺️ 담양 지도")

# Accommodation info - always visible
st.markdown("""
<div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border-radius: 10px; padding: 0.75rem; margin-bottom: 0.75rem;
            border-left: 4px solid #f59e0b; font-size: 0.85rem;">
    <strong>🏡 BASE:</strong> 담양힐링파크 새연리조트 (봉산면) · 🔴 빨간 마커
</div>
""", unsafe_allow_html=True)

# Load data
df = get_venues_df()
accommodation = get_accommodation()

# Category filter (horizontal pills)
st.markdown("**카테고리**")
col1, col2, col3 = st.columns(3)
with col1:
    show_restaurant = st.checkbox("🍚 식당", value=True)
with col2:
    show_cafe = st.checkbox("☕ 카페", value=True)
with col3:
    show_activity = st.checkbox("🎨 Activity", value=True)

# Filter data
categories = []
if show_restaurant:
    categories.append("restaurant")
if show_cafe:
    categories.append("cafe")
if show_activity:
    categories.append("activity")

filtered_df = df[df["category"].isin(categories)] if categories else df

# Show count
st.caption(f"{len(filtered_df)}개 장소 표시")

# Create map
m = folium.Map(
    location=[accommodation["lat"], accommodation["lng"]],
    zoom_start=11,
    tiles="cartodbpositron",
)

# Distance circles
folium.Circle(
    location=[accommodation["lat"], accommodation["lng"]],
    radius=5000,
    color="#3B82F6",
    weight=2,
    fill=True,
    fill_opacity=0.05,
    popup="5km",
).add_to(m)

folium.Circle(
    location=[accommodation["lat"], accommodation["lng"]],
    radius=10000,
    color="#9CA3AF",
    weight=1,
    fill=False,
    popup="10km",
).add_to(m)

# Accommodation marker
folium.Marker(
    location=[accommodation["lat"], accommodation["lng"]],
    popup=f"🏡 {accommodation['name']}",
    icon=folium.Icon(color="red", icon="home", prefix="fa"),
).add_to(m)

# Venue markers
color_map = {"restaurant": "green", "cafe": "orange", "activity": "purple"}
icon_map = {"restaurant": "utensils", "cafe": "coffee", "activity": "palette"}

for _, row in filtered_df.iterrows():
    cat = row["category"]
    popup_text = f"""
    <b>{row['name']}</b><br>
    {row['feature']}<br>
    <small>{row.get('hours', '')}</small>
    """

    folium.Marker(
        location=[row["lat"], row["lng"]],
        popup=folium.Popup(popup_text, max_width=200),
        tooltip=row["name"],
        icon=folium.Icon(
            color=color_map.get(cat, "gray"),
            icon=icon_map.get(cat, "info"),
            prefix="fa",
        ),
    ).add_to(m)

# Render map
st_folium(m, width=None, height=450, use_container_width=True)

# Legend
st.markdown("---")
cols = st.columns(4)
with cols[0]:
    st.caption("🔴 숙소")
with cols[1]:
    st.caption("🟢 식당")
with cols[2]:
    st.caption("🟠 카페")
with cols[3]:
    st.caption("🟣 Activity")

# List of shown venues
st.markdown("---")
st.markdown(f"### 표시된 장소 ({len(filtered_df)})")

for cat in categories:
    cat_df = filtered_df[filtered_df["category"] == cat]
    if not cat_df.empty:
        emoji = CATEGORY_INFO[cat]["emoji"]
        label = CATEGORY_INFO[cat]["label"]
        with st.expander(f"{emoji} {label} ({len(cat_df)})", expanded=False):
            for _, row in cat_df.iterrows():
                st.markdown(f"**{row['name']}** - {row['feature']}")
                if row['url']:
                    st.caption(f"[링크]({row['url']})")
