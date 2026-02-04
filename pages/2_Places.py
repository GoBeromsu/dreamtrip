"""Places List - Mobile First Top-Down Layout."""

import streamlit as st

from utils.data_loader import (
    get_venues_df,
    get_accommodation,
    calculate_distance,
    CATEGORY_INFO,
)

st.set_page_config(
    page_title="장소 목록 - 담양 리트릿",
    page_icon="📋",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
.block-container { padding: 0.5rem 1rem !important; }
</style>
""", unsafe_allow_html=True)

# Back button
if st.button("← 홈으로"):
    st.switch_page("app.py")

st.markdown("## 📋 장소 목록")

# Accommodation info - always visible
st.markdown("""
<div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border-radius: 10px; padding: 0.75rem; margin-bottom: 0.75rem;
            border-left: 4px solid #f59e0b; font-size: 0.85rem;">
    <strong>🏡 BASE:</strong> 담양힐링파크 새연리조트 (봉산면) · 거리순 정렬
</div>
""", unsafe_allow_html=True)

# Load data
df = get_venues_df()
accommodation = get_accommodation()

# Calculate distances
df["distance_km"] = df.apply(
    lambda row: calculate_distance(
        accommodation["lat"], accommodation["lng"],
        row["lat"], row["lng"]
    ),
    axis=1
)

# Search
search = st.text_input("🔍 검색", placeholder="장소명, 특징...")

# Category filter
st.markdown("**카테고리**")
col1, col2, col3 = st.columns(3)
with col1:
    show_restaurant = st.checkbox("🍚 식당", value=True, key="r")
with col2:
    show_cafe = st.checkbox("☕ 카페", value=True, key="c")
with col3:
    show_activity = st.checkbox("🎨 Activity", value=True, key="a")

# Apply filters
categories = []
if show_restaurant:
    categories.append("restaurant")
if show_cafe:
    categories.append("cafe")
if show_activity:
    categories.append("activity")

filtered = df[df["category"].isin(categories)] if categories else df

if search:
    search_lower = search.lower()
    filtered = filtered[
        filtered["name"].str.lower().str.contains(search_lower, na=False) |
        filtered["feature"].str.lower().str.contains(search_lower, na=False)
    ]

# Sort by distance
filtered = filtered.sort_values("distance_km")

st.caption(f"{len(filtered)}개 장소")
st.markdown("---")

# Display venues in top-down cards
for _, row in filtered.iterrows():
    cat = row["category"]
    cat_info = CATEGORY_INFO.get(cat, {"emoji": "", "label": cat, "color": "#6b7280"})

    with st.container():
        # Category badge + Name
        st.markdown(
            f"<span style='background:{cat_info['color']}15; color:{cat_info['color']}; "
            f"padding:2px 8px; border-radius:4px; font-size:0.7rem;'>"
            f"{cat_info['emoji']} {cat_info['label']}</span>",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**{row['name']}**")
            st.caption(f"{row['feature']}")

            # Hours + Distance
            info_parts = []
            if row.get('hours'):
                info_parts.append(f"🕐 {row['hours']}")
            info_parts.append(f"📍 {row['distance_km']:.1f}km")
            st.caption(" · ".join(info_parts))

            # Note if exists
            if row.get('note'):
                st.caption(f"💡 {row['note']}")

        with col2:
            if row['url']:
                st.link_button("🔗", row['url'], use_container_width=True)

        st.markdown("---")

# Download CSV
if st.button("📥 CSV 다운로드"):
    csv_df = filtered[["name", "category", "feature", "address", "hours", "distance_km"]]
    csv_df.columns = ["장소명", "카테고리", "특징", "주소", "운영시간", "거리(km)"]
    csv = csv_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="다운로드",
        data=csv,
        file_name="damyang_venues.csv",
        mime="text/csv",
    )
