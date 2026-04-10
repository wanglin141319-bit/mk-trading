from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630

# 颜色
BG       = (5, 6, 15)       # #05060f
ACCENT   = (0, 212, 255)    # #00d4ff
ACCENT2  = (123, 97, 255)  # #7b61ff
GREEN    = (0, 255, 136)   # #00ff88
GOLD     = (255, 215, 0)   # #ffd700
TEXT     = (232, 234, 240) # #e8eaf0
TEXT_DIM = (107, 114, 128) # #6b7280

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# ---- 辅助：画渐变背景线条 ----
for i in range(H):
    alpha = i / H
    r = int(5 + alpha * 10)
    g = int(6 + alpha * 15)
    b = int(15 + alpha * 25)
    draw.line([(0, i), (W, i)], fill=(r, g, b))

# ---- 背景网格 ----
for x in range(0, W, 60):
    draw.line([(x, 0), (x, H)], fill=(20, 22, 40), width=1)
for y in range(0, H, 60):
    draw.line([(0, y), (W, y)], fill=(20, 22, 40), width=1)

# ---- 装饰圆 ----
def glow_circle(x, y, r, col, intensity=0.08):
    for i in range(r, 0, -1):
        alpha = intensity * (1 - i / r)
        draw.ellipse([x-i, y-i, x+i, y+i], fill=col + (int(alpha * 255),) if len(col) == 3 else None)

# 左上角光晕
for i in range(200, 0, -1):
    alpha = 0.003 * (1 - i / 200)
    col = (0, int(212 * alpha * 3), int(255 * alpha * 3))
    draw.ellipse([100-i, 80-i, 100+i, 80+i], fill=col)

# 右上角光晕
for i in range(180, 0, -1):
    alpha = 0.003 * (1 - i / 180)
    col = (int(123 * alpha * 3), int(97 * alpha * 3), int(255 * alpha * 3))
    draw.ellipse([W-100-i, 100-i, W-100+i, 100+i], fill=col)

# ---- 小星星 ----
import random
random.seed(42)
stars = [(random.randint(0, W), random.randint(0, H), random.uniform(0.5, 2)) for _ in range(80)]
for sx, sy, sr in stars:
    draw.ellipse([sx, sy, sx+sr, sy+sr], fill=(200, 210, 255))

# ---- 字体加载 ----
font_paths = [
    "C:/Windows/Fonts/Orbitron/Orbitron-Bold.ttf",
    "C:/Windows/Fonts/Orbitron/Orbitron-Regular.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/seguisb.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]

def get_font(size, bold=False):
    candidates = [
        f"C:/Windows/Fonts/Orbitron/Orbitron-{'Bold' if bold else 'Regular'}.ttf",
        f"C:/Windows/Fonts/arial{'bd' if bold else ''}.ttf",
        "C:/Windows/Fonts/seguisb.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()

font_large  = get_font(100, bold=True)   # MK logo
font_mid    = get_font(28, bold=False)   # MK TRADING
font_stat_v = get_font(56, bold=True)    # 数字
font_stat_l = get_font(18, bold=False)   # 标签
font_tag    = get_font(22, bold=False)   # tagline
font_small  = get_font(14, bold=False)   # 底部文字

# ---- MK Logo ----
logo_x = W // 2
logo_y = 110

# 发光层
for blur in [8, 4, 2]:
    glow_img = Image.new("RGBA", (W, H), (0,0,0,0))
    glow_draw = ImageDraw.Draw(glow_img)
    glow_draw.text((logo_x, logo_y), "MK", font=font_large, anchor="mm",
                   fill=(0, 212, 255, 60 // blur))
    img.paste(glow_img, (0, 0), glow_img)

draw.text((logo_x, logo_y), "MK", font=font_large, anchor="mm", fill=TEXT)

# ---- MK TRADING ----
draw.text((logo_x, logo_y + 65), "MK  TRADING", font=font_mid, anchor="mm",
          fill=(0, 212, 255))

# ---- 分隔线 ----
line_y = logo_y + 110
draw.line([(W//2 - 200, line_y), (W//2 + 200, line_y)], fill=(0, 212, 255, 100), width=1)

# ---- 三个数据 ----
stats = [
    ("+312%", "年化收益率", GREEN),
    ("88%", "胜率", ACCENT),
    ("2.8:1", "盈亏比", GOLD),
]

stat_start_x = W // 2 - 300
stat_gap = 300

for i, (val, label, col) in enumerate(stats):
    sx = stat_start_x + i * stat_gap + 150
    sy = logo_y + 175

    # 数值
    draw.text((sx, sy), val, font=font_stat_v, anchor="mm", fill=col)

    # 标签
    draw.text((sx, sy + 40), label, font=font_stat_l, anchor="mm", fill=TEXT_DIM)

    # 下划线装饰
    uw = 80
    draw.line([(sx - uw//2, sy + 65), (sx + uw//2, sy + 65)], col, width=2)

# ---- 底部 Tagline ----
tagline = "专注BTC / ETH / SOL 合约交易  ·  数据驱动  ·  纪律优先"
draw.text((W//2, H - 80), tagline, font=font_tag, anchor="mm", fill=TEXT)

# ---- 底部免责声明 ----
draw.text((W//2, H - 45), "MKtrading.vip  |  过往收益不代表未来表现，投资有风险", font=font_small, anchor="mm", fill=TEXT_DIM)

# ---- 保存 ----
out_path = "C:/Users/asus/mk-trading/og-image.png"
img.save(out_path, "PNG", optimize=True)
print(f"Saved: {out_path}")
