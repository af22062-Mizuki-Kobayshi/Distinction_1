import tkinter as tk
from itertools import permutations

# 人の名前と色
people = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta']
people_data = list(zip(people, colors))

# A, B, C の並び替え（6通り）
room_orders = list(permutations(['A', 'B', 'C']))
room_fixed = ['A', 'B', 'C', 'D']

# グループインデックス：a,b / c,d / e,f / g（→D部屋）
group_indices = {
    0: [0, 1],
    1: [2, 3],
    2: [4, 5],
    3: [6],  # g
}

# Tkinter 初期化
root = tk.Tk()
root.title("固定4部屋・6パターン配置（gはD部屋）")

# 画面サイズを手動指定（必要に応じて） # ← 変更ポイント（画面サイズを明示）
root.geometry("1920x1080")  # コメントアウトして root.state('zoomed') でも可
root.update_idletasks()

# メインフレーム（左右2分割）
main_frame = tk.Frame(root)
main_frame.pack(fill='both', expand=True, padx=20, pady=20)

screen_width = root.winfo_screenwidth()
half_width = screen_width // 2 - 40

left_frame = tk.Frame(main_frame, width=half_width)
left_frame.grid(row=0, column=0, sticky='n')

right_frame = tk.Frame(main_frame, width=half_width)
right_frame.grid(row=0, column=1, sticky='n')

# 各パターンを表示
for idx, order in enumerate(room_orders):
    target_parent = left_frame if idx < 3 else right_frame
    row_idx = idx if idx < 3 else idx - 3

    pattern_frame = tk.LabelFrame(
        target_parent,
        text=f"パターン {idx + 1}: {order + ('D',)}",
        font=('Arial', 14, 'bold'),
        padx=10,
        pady=10
    )
    pattern_frame.grid(row=row_idx, column=0, pady=20)  # ← 変更ポイント（縦スペース広め）

    # 各部屋フレームの設定（固定順 A〜D）
    room_frames = {}
    for i, room in enumerate(room_fixed):
        frame = tk.LabelFrame(
            pattern_frame,
            text=f"部屋 {room}",
            width=250,      # ← 変更ポイント（横幅拡大）
            height=180,     # ← 変更ポイント（縦幅拡大）
            padx=10,
            pady=10
        )
        frame.grid(row=0, column=i, padx=5)
        frame.grid_propagate(False)
        room_frames[room] = frame

    # 人の割り当て（g → D固定）
    assignments = {r: [] for r in room_fixed}
    assignments['D'] = group_indices[3]
    for group_idx, room_label in enumerate(order):
        assignments[room_label] = group_indices[group_idx]

    # ラベル（人）を各部屋に配置
    for room, indices in assignments.items():
        for i in indices:
            name, color = people_data[i]
            label = tk.Label(
                room_frames[room],
                text=name,
                bg=color,
                fg='white',
                font=('Arial', 20, 'bold'),  # ← 変更ポイント（フォントサイズと太字）
                width=2,                      # ← 変更ポイント（ラベル横幅拡大）
                height=1,                     # ← 変更ポイント（ラベル縦幅拡大）
                relief='raised'
            )
            label.pack(side='left', padx=10, pady=10)  # ← 変更ポイント（余白拡大）

# 明示的に左右の幅を設定（スクリーン半分を確保） # ← 変更ポイント
left_frame.config(width=half_width)
right_frame.config(width=half_width)

root.mainloop()
