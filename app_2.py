import streamlit as st
from itertools import permutations
from collections import defaultdict

# 色設定
COLORS = ['lightblue', 'lightgreen', 'lightpink', 'lightyellow', 'orange']
GRAY_COLOR = '#e0e0e0'

st.set_page_config(layout="wide")
st.title("部屋割り30通り表示アプリ")

# 入力欄（5人）
st.subheader("名前を5人分入力してください")
cols = st.columns(5)
names = [col.text_input(f"名前{i+1}", key=f"name_{i}").strip() for i, col in enumerate(cols)]

# 有効な名前だけ使う
valid_names = [n for n in names if n]
if len(valid_names) != 5:
    st.warning("5人すべての名前を入力してください。")
    st.stop()

name_color = {name: COLORS[i] for i, name in enumerate(valid_names)}

# 30通り生成（部屋順を考慮）
def generate_all_30_patterns(names):
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

# 表示モード選択
mode = st.radio("表示モード", ["部屋区別あり", "部屋区別なし（重複グループ化＋クリックで灰色）"])

# グレー表示状態保持
if 'gray_flags' not in st.session_state:
    st.session_state.gray_flags = [False] * len(patterns)

# HTMLスタイル表示関数
def display_room_pattern(roomA, roomB, roomC, name_color, label, idx=None, gray=False, show_labels=True):
    rooms = [roomA, roomB, roomC]
    labels = ["部屋 A", "部屋 B", "部屋 C"] if show_labels else ["部屋"] * 3
    html = f"<div style='border:1px solid gray; padding:10px; margin:10px; width:450px;'>"
    html += f"<h4 style='margin:0; cursor:pointer;' id='title-{idx}'>{label}</h4><div style='display:flex; justify-content:space-between;'>"

    for i in range(3):
        html += "<div><b>{}</b><br>".format(labels[i])
        for name in rooms[i]:
            color = GRAY_COLOR if gray else name_color[name]
            html += f"<div style='display:inline-block; background-color:{color}; color:black; padding:10px; "
            html += f"margin:5px; border-radius:20px; font-size:14px; font-weight:bold;'>{name}</div><br>"
        html += "</div>"
    html += "</div></div>"
    return html

# 区別ありモード
if mode == "部屋区別あり":
    st.subheader("部屋区別ありの30通り")
    for i in range(0, len(patterns), 2):
        col1, col2 = st.columns(2)
        for col, pattern in zip([col1, col2], patterns[i:i+2]):
            roomA, roomB, roomC = pattern
            html = display_room_pattern(roomA, roomB, roomC, name_color, f"パターン {i + 1 if col == col1 else i + 2}", show_labels=True)
            col.markdown(html, unsafe_allow_html=True)

# 区別なしモード（同一組み合わせをグループ化し、初回以外はグレー）
else:
    st.subheader("部屋区別なし（同一構成をグループ化）")
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
            gray = (j > 0)  # 2つ目以降は灰色
            label = f"パターン {group_idx+1}-{j+1}"
            html = display_room_pattern(roomA, roomB, roomC, name_color, label, idx=idx, gray=gray, show_labels=False)
            cols[j].markdown(html, unsafe_allow_html=True)
            idx += 1
