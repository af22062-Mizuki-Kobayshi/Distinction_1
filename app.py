import streamlit as st
from itertools import permutations

# 人の名前と色
people = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta']
people_data = list(zip(people, colors))

# 並び順
room_orders = list(permutations(['A', 'B', 'C']))
room_fixed = ['A', 'B', 'C', 'D']

# グループごとのインデックス
group_indices = {
    0: [0, 1],
    1: [2, 3],
    2: [4, 5],
    3: [6],  # g
}

st.set_page_config(layout="wide")
st.title("固定4部屋・6パターン配置（gはD部屋）")

# 画面を2列に分割
col_left, col_right = st.columns(2)

for idx, order in enumerate(room_orders):
    target_col = col_left if idx < 3 else col_right

    with target_col:
        st.markdown(f"### パターン {idx+1}: {order + ('D',)}")
        colA, colB, colC, colD = st.columns(4)
        room_cols = {'A': colA, 'B': colB, 'C': colC, 'D': colD}

        # 割り当て処理
        assignments = {r: [] for r in room_fixed}
        assignments['D'] = group_indices[3]
        for group_idx, room_label in enumerate(order):
            assignments[room_label] = group_indices[group_idx]

        # 表示処理
        for room in room_fixed:
            with room_cols[room]:
                st.markdown(f"**部屋 {room}**")
                for i in assignments[room]:
                    name, color = people_data[i]
                    st.markdown(
                        f"<div style='display:inline-block; background-color:{color}; "
                        f"color:white; padding:10px 20px; margin:5px; border-radius:5px; "
                        f"font-weight:bold; font-size:20px;'>{name}</div>",
                        unsafe_allow_html=True
                    )
