import streamlit as st
from itertools import permutations
from collections import defaultdict

COLORS = ['lightblue', 'lightgreen', 'lightpink', 'lightyellow', 'orange']
GRAY_COLOR = '#e0e0e0'

st.set_page_config(layout="wide")
st.title("部屋割り")

# 入力欄（5人）
st.subheader("出席番号を5人分入力してください")
cols = st.columns(5)
names = [col.text_input(f"名前{i+1}", key=f"name_{i}").strip() for i, col in enumerate(cols)]

valid_names = [n for n in names if n]
if len(valid_names) != 5:
    st.warning("5人すべての出席番号を入力してください。")
    st.stop()

name_color = {name: COLORS[i] for i, name in enumerate(valid_names)}

def generate_all_30_patterns(names):
    if len(names) != 5:
        return []
    patterns = []
    seen = set()
    for perm in permutations(names):
        roomA = tuple(sorted(perm[0:2]))
        roomB = tuple(sorted(perm[2:4]))
        roomC = (perm[4],)
        pattern = (roomA, roomB, roomC)
        if pattern not in seen:
            patterns.append(pattern)
            seen.add(pattern)
    return patterns

patterns = generate_all_30_patterns(valid_names)

mode = st.radio("表示モード", ["部屋区別あり", "部屋区別なし"])

if 'gray_flags' not in st.session_state:
    st.session_state.gray_flags = {}

def display_room_pattern(roomA, roomB, roomC, name_color, gray=False, show_labels=True):
    rooms = [roomA, roomB, roomC]
    labels = ["部屋 A", "部屋 B", "部屋 C"] if show_labels else ["部屋"] * 3
    html = f"<div style='border:1px solid gray; padding:10px; margin-top:5px; width:450px;'>"
    html += "<div style='display:flex; justify-content:space-between;'>"

    for i in range(3):
        html += "<div><b>{}</b><br>".format(labels[i])
        for name in rooms[i]:
            color = GRAY_COLOR if gray else name_color[name]
            html += f"<div style='display:inline-block; background-color:{color}; color:black; padding:10px; "
            html += f"margin:5px; border-radius:20px; font-size:14px; font-weight:bold;'>{name}</div><br>"
        html += "</div>"
    html += "</div></div>"
    return html

if mode == "部屋区別あり":
    st.subheader("部屋区別あり")
    for i in range(0, len(patterns), 2):
        col1, col2 = st.columns(2)
        for col, pattern in zip([col1, col2], patterns[i:i+2]):
            roomA, roomB, roomC = pattern
            html = display_room_pattern(roomA, roomB, roomC, name_color, gray=False, show_labels=True)
            col.markdown(f"### パターン {i + 1 if col == col1 else i + 2}")
            col.markdown(html, unsafe_allow_html=True)

else:
    st.subheader("部屋区別なし")
    grouped = defaultdict(list)
    for pattern in patterns:
        roomA, roomB, roomC = pattern
        key = frozenset([frozenset(roomA), frozenset(roomB), frozenset(roomC)])
        grouped[key].append(pattern)

    idx = 0
    for group_idx, group in enumerate(grouped.values()):
        cols = st.columns(len(group))
        for j, pattern in enumerate(group):
            roomA, roomB, roomC = pattern
            pattern_key = f"pattern_{idx}"
            if pattern_key not in st.session_state.gray_flags:
                st.session_state.gray_flags[pattern_key] = False

            button_label = f"パターン {group_idx+1}-{j+1}"
            if cols[j].button(button_label, key=f"btn_{pattern_key}"):
                st.session_state.gray_flags[pattern_key] = not st.session_state.gray_flags[pattern_key]

            gray = st.session_state.gray_flags[pattern_key]
            html = display_room_pattern(roomA, roomB, roomC, name_color, gray=gray, show_labels=False)
            cols[j].markdown(html, unsafe_allow_html=True)
            idx += 1
