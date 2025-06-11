import streamlit as st
from itertools import permutations

# 色の定義（5人分）
COLORS = ['lightblue', 'lightgreen', 'lightpink', 'lightyellow', 'orange']

st.set_page_config(layout="wide")
st.title("部屋割り（5人→3部屋：30通り表示）")

# 名前の入力
st.subheader("名前を5人分入力してください")
cols = st.columns(5)
names = []
for i, col in enumerate(cols):
    name = col.text_input(f"名前{i + 1}", key=f"name_{i}")
    names.append(name.strip())

# チェックと処理
valid_names = [n for n in names if n]
if len(valid_names) != 5:
    st.warning("5人すべての名前を入力してください。")
    st.stop()

# 名前と色を対応づけ
name_color = {name: COLORS[i] for i, name in enumerate(valid_names)}

# パターン生成関数
def generate_all_30_patterns(names):
    patterns = set()
    for perm in permutations(names):
        roomA = tuple(sorted(perm[0:2]))
        roomB = tuple(sorted(perm[2:4]))
        roomC = (perm[4],)
        patterns.add((roomA, roomB, roomC))
    return sorted(patterns)

# パターンを生成
patterns = generate_all_30_patterns(valid_names)

# 表示
st.subheader("部屋割り30通り（順不同を除外）")
for idx in range(0, len(patterns), 2):
    col1, col2 = st.columns(2)

    for col, pattern in zip([col1, col2], patterns[idx:idx+2]):
        with col:
            roomA, roomB, roomC = pattern
            st.markdown(f"### パターン {idx + 1 if col == col1 else idx + 2}")

            rcols = st.columns(3)
            for room_col, room_name, members in zip(rcols, ["部屋 A", "部屋 B", "部屋 C"], [roomA, roomB, roomC]):
                with room_col:
                    st.markdown(f"**{room_name}**")
                    for member in members:
                        st.markdown(
                            f"<div style='display:inline-block; background-color:{name_color[member]}; "
                            f"color:black; padding:10px 20px; margin:5px; border-radius:20px; "
                            f"font-size:16px; font-weight:bold;'>{member}</div>",
                            unsafe_allow_html=True
                        )
