from datetime import datetime
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

if getattr(sys, 'frozen', False):
    # PyInstaller でビルドされた .exe 実行中
    base_dir = os.path.dirname(sys.executable)
else:
    # 通常の Python 実行中
    base_dir = os.getcwd()

# Tkinterのルートウィンドウを隠す
root = tk.Tk()
root.withdraw()

# ファイル選択ダイアログを表示（画像ファイルを選ぶ）
file_path = filedialog.askopenfilename(
    title="Select Image",
    filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff")]
)

# 選ばなかった場合
if not file_path:
    print("画像が選択されませんでした。処理を終了します。")
    exit()

# 選んだ画像を読み込む
image = cv2.imread(file_path)
if image is None:
    print("画像の読み込みに失敗しました。")
    exit()
image_display = image.copy()

# BGR → RGB に変換（matplotlib表示用）
image_rgb = cv2.cvtColor(image_display, cv2.COLOR_BGR2RGB)

# 座標保存用リスト
clicked_points = []

# 順序を整える関数
'''
# 従来の順序を整える関数
def order_points(pts):
    pts = np.array(pts, dtype="float32")
    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1)

    ordered = np.zeros((4, 2), dtype="float32")
    ordered[0] = pts[np.argmin(s)]       # 左上: 最小の合計
    ordered[2] = pts[np.argmax(s)]       # 右下: 最大の合計
    ordered[1] = pts[np.argmin(diff)]    # 右上: 最小の差
    ordered[3] = pts[np.argmax(diff)]    # 左下: 最大の差
    return ordered
'''

# 新しい順序を整える関数
# ユークリッド距離＋重心からの角度に基づく分類で順序を変更する
def order_points_by_angle(pts):
    pts = np.array(pts, dtype="float32")
    center = np.mean(pts, axis=0)
    # 各点から重心へのベクトル角度を取得（反時計回り）
    angles = np.arctan2(pts[:,1] - center[1], pts[:,0] - center[0])
    # 角度でソート
    ordered = pts[np.argsort(angles)]
    # 左上から開始するように並び替え
    # 最も「左上」に近い点を探す（最小 x+y）
    idx_topleft = np.argmin(np.sum(ordered, axis=1))
    ordered = np.roll(ordered, -idx_topleft, axis=0)
    return ordered

# クリックイベント
def on_click(event):
    if event.inaxes:
        x, y = int(event.xdata), int(event.ydata)
        clicked_points.append((x, y))
        print(f"Clicked at: ({x}, {y})")
        ax.plot(x, y, 'ro')
        fig.canvas.draw()
        if len(clicked_points) == 4:
            plt.close()  # 4点クリックでウィンドウ閉じる

# 画像表示とクリック受付
fig, ax = plt.subplots()
ax.imshow(image_rgb)
ax.set_title("Click 4 points (corners of the quadrat)")
cid = fig.canvas.mpl_connect('button_press_event', on_click)
plt.show()

if len(clicked_points) != 4:
    print("4点が選択されていません。処理を終了します。")
    exit()

# 順序補正
#pts_src = order_points(clicked_points)
pts_src = order_points_by_angle(clicked_points)

# 出力画像サイズ（任意で調整）
width, height = 1000, 1000
pts_dst = np.array([
    [0, 0],
    [width - 1, 0],
    [width - 1, height - 1],
    [0, height - 1]
], dtype='float32')

# 射影変換と適用
M = cv2.getPerspectiveTransform(pts_src, pts_dst)
warped = cv2.warpPerspective(image, M, (width, height))

# 表示
#warped_rgb = cv2.cvtColor(warped, cv2.COLOR_BGR2RGB)
#plt.imshow(warped_rgb)
#plt.axis('off')
#plt.title("Warped Image (Top-down View)")
#plt.show()

# HSVに変換
hsv = cv2.cvtColor(warped, cv2.COLOR_BGR2HSV)

cv2.namedWindow("Mask Comparison", cv2.WINDOW_NORMAL)

def nothing(x): pass

# スライダー作成
cv2.createTrackbar("H min", "Mask Comparison", 35, 179, nothing)
cv2.createTrackbar("H max", "Mask Comparison", 95, 179, nothing)
cv2.createTrackbar("S min", "Mask Comparison", 0, 255, nothing)
cv2.createTrackbar("S max", "Mask Comparison", 255, 255, nothing)
cv2.createTrackbar("V min", "Mask Comparison", 0, 255, nothing)
cv2.createTrackbar("V max", "Mask Comparison", 255, 255, nothing)

while True:
    # スライダー取得
    hmin = cv2.getTrackbarPos("H min", "Mask Comparison")
    hmax = cv2.getTrackbarPos("H max", "Mask Comparison")
    smin = cv2.getTrackbarPos("S min", "Mask Comparison")
    smax = cv2.getTrackbarPos("S max", "Mask Comparison")
    vmin = cv2.getTrackbarPos("V min", "Mask Comparison")
    vmax = cv2.getTrackbarPos("V max", "Mask Comparison")

    # マスクとマスク画像作成
    lower = np.array([hmin, smin, vmin])
    upper = np.array([hmax, smax, vmax])
    mask = cv2.inRange(hsv, lower, upper)
    masked = cv2.bitwise_and(warped, warped, mask=mask)

    # リサイズ（表示用）
    display_left = cv2.resize(masked, (500, 500))
    display_right = cv2.resize(warped, (500, 500))
    display = np.hstack((display_left, display_right))

    # 割合計算
    total_pixels = mask.shape[0] * mask.shape[1]
    green_pixels = cv2.countNonZero(mask)
    other_pixels = total_pixels - green_pixels
    green_ratio = 100 * green_pixels / total_pixels
    other_ratio = 100 * other_pixels / total_pixels

    # 下にスペースを作ってテキストを描画する
    padding = 50
    annotated = cv2.copyMakeBorder(display, 0, padding, 0, 0, cv2.BORDER_CONSTANT, value=(255, 255, 255))

    text = f"Green: {green_ratio:.2f}% | Other: {other_ratio:.2f}%"
    cv2.putText(
        annotated,
        text,
        (10, display.shape[0] + 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 0),
        1,
        cv2.LINE_AA
    )

    # 表示
    cv2.imshow("Mask Comparison", annotated)

    # 'q'で終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

hmin_green = hmin
hmax_green = hmax
smin_green = smin
smax_green = smax
vmin_green = vmin
vmax_green = vmax

# リターと地面の判別処理

mask_green = mask.copy()
mask_not_green = cv2.bitwise_not(mask_green)  # 緑以外の領域

cv2.namedWindow("Litter Classifier", cv2.WINDOW_NORMAL)

def nothing(x): pass

# --- スライダー（リターのHSV調整用）---
cv2.createTrackbar("H min", "Litter Classifier", 0, 179, nothing)
cv2.createTrackbar("H max", "Litter Classifier", 179, 179, nothing)
cv2.createTrackbar("S min", "Litter Classifier", 0, 255, nothing)
cv2.createTrackbar("S max", "Litter Classifier", 255, 255, nothing)
cv2.createTrackbar("V min", "Litter Classifier", 0, 255, nothing)
cv2.createTrackbar("V max", "Litter Classifier", 150, 255, nothing)

while True:
    # スライダー値取得
    hmin = cv2.getTrackbarPos("H min", "Litter Classifier")
    hmax = cv2.getTrackbarPos("H max", "Litter Classifier")
    smin = cv2.getTrackbarPos("S min", "Litter Classifier")
    smax = cv2.getTrackbarPos("S max", "Litter Classifier")
    vmin = cv2.getTrackbarPos("V min", "Litter Classifier")
    vmax = cv2.getTrackbarPos("V max", "Litter Classifier")

    # リター抽出（非緑マスクとAND）
    lower_litter = np.array([hmin, smin, vmin])
    upper_litter = np.array([hmax, smax, vmax])
    mask_litter = cv2.inRange(hsv, lower_litter, upper_litter)
    mask_litter = cv2.bitwise_and(mask_litter, mask_not_green)

    # --- 地面（＝緑以外 − リター） ---
    mask_soil = cv2.bitwise_and(mask_not_green, cv2.bitwise_not(mask_litter))

    # --- 背景画像（緑領域を黒く塗りつぶす） ---
    background = warped.copy()
    background[mask_green > 0] = (50, 50, 50)

    # --- リターを塗りつぶした画像（左側） ---
    vis_litter = background.copy()
    vis_litter[mask_litter > 0] = (0, 0, 0)
    
    # --- 緑だけ白で消した比較画像（右側） ---
    vis_compare = background.copy()

    # --- リサイズと横並べ表示 ---
    vis_litter_resized = cv2.resize(vis_litter, (500, 500))
    vis_compare_resized = cv2.resize(vis_compare, (500, 500))
    combined = np.hstack((vis_litter_resized, vis_compare_resized))

    # --- 割合計算 ---
    total = warped.shape[0] * warped.shape[1]
    g_pix = cv2.countNonZero(mask_green)
    l_pix = cv2.countNonZero(mask_litter)
    s_pix = cv2.countNonZero(mask_soil)

    # --- 下部に割合を描画するエリアを追加 ---
    combined_annotated = cv2.copyMakeBorder(combined, 0, 50, 0, 0, cv2.BORDER_CONSTANT, value=(255,255,255))
    text = f"Green: {g_pix/total*100:.2f}% | Litter: {l_pix/total*100:.2f}% | Soil: {s_pix/total*100:.2f}%"
    cv2.putText(combined_annotated, text, (10, combined.shape[0]+30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 1, cv2.LINE_AA)

    # --- 表示 ---
    cv2.imshow("Litter Classifier", combined_annotated)

    # 終了キー
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

green_ratio = g_pix/total
litter_ratio = l_pix/total
soil_ratio = s_pix/total

time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
# ファイルパスを相対パスで保存する
relative_path = os.path.relpath(file_path)

# 拡張子を除いたファイル名を取得
basename_with_ext = os.path.basename(file_path)
basename = os.path.splitext(basename_with_ext)[0]

# 保存データ
df = pd.DataFrame({
    "file_path": [relative_path],
    "file_name": [basename_with_ext],
    "time": [time],
    "green_ratio": [green_ratio],
    "litter_ratio": [litter_ratio],
    "soil_ratio": [soil_ratio],
    "hmin_green": [hmin_green],
    "hmax_green": [hmax_green],
    "smin_green": [smin_green],
    "smax_green": [smax_green],
    "vmin_green": [vmin_green],
    "vmax_green": [vmax_green],
    "hmin_litter": [hmin],
    "hmax_litter": [hmax],
    "smin_litter": [smin],
    "smax_litter": [smax],
    "vmin_litter": [vmin],
    "vmax_litter": [vmax],
})

#csv_path = "output/classify_quadrat_regions.csv"
csv_path = os.path.join(base_dir, "output", "classify_quadrat_regions.csv")

if os.path.exists(csv_path):
    # 既存CSVを読み込み
    existing_data = pd.read_csv(csv_path)

    # IDをキーにして更新（重複IDはnew_dataで上書き）
    combined = pd.concat([existing_data, df], ignore_index=True)
    combined = combined.drop_duplicates(subset="file_name", keep="last")  # 最新のものを残す
else:
    # 新規作成
    combined = df

# 保存（上書き保存）
combined.to_csv(csv_path, index=False, encoding="utf-8")

# 画像の保存 ---

#save_dir_warped = "output/figures/quadrat_warped"
save_dir_warped = os.path.join(base_dir, "output", "figures", "quadrat_warped")
# フォルダが存在しない場合は作成
if not os.path.exists(save_dir_warped):
    os.makedirs(save_dir_warped)
# 画像を保存
save_path = os.path.join(save_dir_warped, basename + '.jpg')
cv2.imwrite(save_path, warped)

# 保存用のセグメント画像を作成(色はBGRでの指定であることに注意)
segment_green = warped.copy()
segment_green[mask_green > 0] = (180, 180, 0)

segment_litter = segment_green
segment_litter[mask_litter > 0] = (0, 170, 255)

segment_soil = segment_litter.copy()
# 植物でもリターでもない部分を地面とみなす
mask_soil = np.logical_and(mask_green == 0, mask_litter == 0)
segment_soil[mask_soil] = (204, 102, 153)

#save_dir_segmented = "output/figures/quadrat_segmented"
save_dir_segmented = os.path.join(base_dir, "output", "figures", "quadrat_segmented")
# フォルダが存在しない場合は作成
if not os.path.exists(save_dir_segmented):
    os.makedirs(save_dir_segmented)
# 画像を保存
save_path = os.path.join(save_dir_segmented, basename + '.jpg')
cv2.imwrite(save_path, segment_soil)
