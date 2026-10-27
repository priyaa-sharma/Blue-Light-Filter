import atexit
import ctypes
import math
import tkinter as tk
from ctypes import wintypes

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
user32.GetDC.restype = wintypes.HDC
user32.GetDC.argtypes = [wintypes.HWND]
user32.ReleaseDC.argtypes = [wintypes.HWND, wintypes.HDC]
gdi32.SetDeviceGammaRamp.argtypes = [wintypes.HDC, ctypes.c_void_p]
gdi32.SetDeviceGammaRamp.restype = wintypes.BOOL

MIN_SCALE = 0.5

PINK = "#FF8DA1"
PEACH = "#FFC2BA"
PETAL = "#FF9CE9"
PURPLE = "#AD56C4"
INK = "#49264F"
BACKGROUND = "#ffc2ba"
CARD = "#FFFEFF"
MUTED = "#855E78"
TRACK = "#F6DCE8"
STATUS_BACKGROUND = "#FFEAF2"


def kelvin_to_rgb(k):
    t = k / 100
    r = 255 if t <= 66 else 329.698727446 * (t - 60) ** -0.1332047592
    g = (99.4708025861 * math.log(t) - 161.1195681661) if t <= 66 \
        else 288.1221695283 * (t - 60) ** -0.0755148492
    if t >= 66:
        b = 255
    elif t <= 19:
        b = 0
    else:
        b = 138.5177312231 * math.log(t - 10) - 305.0447927307
    return tuple(max(0, min(255, v)) / 255 for v in (r, g, b))


def set_ramp(scales):
    ramp = ((ctypes.c_ushort * 256) * 3)()
    for ch in range(3):
        scale = max(MIN_SCALE, min(1.0, scales[ch]))
        for i in range(256):
            ramp[ch][i] = int(i * 257 * scale)
    hdc = user32.GetDC(None)
    ok = gdi32.SetDeviceGammaRamp(hdc, ctypes.byref(ramp))
    user32.ReleaseDC(None, hdc)
    return bool(ok)


def reset():
    set_ramp((1.0, 1.0, 1.0))


atexit.register(reset)

root = tk.Tk()
root.title("Blue light filter")
root.geometry("460x590")
root.resizable(False, False)
root.configure(bg=BACKGROUND)

temp = tk.IntVar(value=3600)
dim = tk.IntVar(value=0)
enabled = tk.BooleanVar(value=True)
status = tk.StringVar()
temperature_value = tk.StringVar()
dim_value = tk.StringVar()


def apply(*_):
    temperature_value.set(f"{temp.get():,} K")
    dim_value.set(f"{dim.get()}%")
    if not enabled.get():
        reset()
        status.set("Your display is back to its natural colour.")
        status_label.configure(fg=INK)
        return
    r, g, b = kelvin_to_rgb(temp.get())
    brightness = 1 - dim.get() / 100
    ok = set_ramp((r * brightness, g * brightness, b * brightness))
    if ok:
        status.set("Filter is active  ·  Changes apply instantly")
        status_label.configure(fg=INK)
    else:
        status.set("Windows rejected this setting. Try a higher temperature.")
        status_label.configure(fg=INK)


def toggle_filter():
    enabled.set(not enabled.get())
    toggle_button.configure(
        text="FILTER ON" if enabled.get() else "FILTER OFF",
        bg=INK if enabled.get() else PURPLE,
    )
    apply()


def preset(temperature, dimming):
    temp.set(temperature)
    dim.set(dimming)
    enabled.set(True)
    toggle_button.configure(text="FILTER ON", bg=INK)
    apply()


shell = tk.Frame(root, bg=BACKGROUND)
shell.pack(fill="both", expand=True, padx=22, pady=18)

header = tk.Frame(shell, bg=PURPLE, padx=20, pady=17)
header.pack(fill="x")
header_content = tk.Frame(header, bg=PURPLE)
header_content.pack(fill="x")
header_text = tk.Frame(header_content, bg=PURPLE)
header_text.pack(side="left", fill="both", expand=True, pady=5)
tk.Label(
    header_text,
    text="DISPLAY WELLNESS",
    font=("Segoe UI", 9, "bold"),
    fg=PEACH,
    bg=PURPLE,
).pack(anchor="w")
tk.Label(
    header_text,
    text="Blue light filter",
    font=("Segoe UI", 22, "bold"),
    fg="#FFFFFF",
    bg=PURPLE,
).pack(anchor="w", pady=(2, 0))
tk.Label(
    header_text,
    text="A warmer screen, whenever you need it.",
    font=("Segoe UI", 10),
    fg="#FFF5F8",
    bg=PURPLE,
).pack(anchor="w", pady=(2, 0))

sun_doodle = tk.Canvas(
    header_content,
    width=104,
    height=104,
    bg=PURPLE,
    bd=0,
    highlightthickness=0,
)
sun_doodle.pack(side="right", padx=(0, 0))
sun_center = (53, 51)
sun_radius = 25
for angle in range(0, 360, 45):
    radians = math.radians(angle)
    inner_x = sun_center[0] + math.cos(radians) * (sun_radius + 7)
    inner_y = sun_center[1] + math.sin(radians) * (sun_radius + 7)
    outer_x = sun_center[0] + math.cos(radians) * (sun_radius + 14)
    outer_y = sun_center[1] + math.sin(radians) * (sun_radius + 14)
    sun_doodle.create_line(
        inner_x,
        inner_y,
        outer_x,
        outer_y,
        fill=PEACH,
        width=2,
        capstyle=tk.ROUND,
    )
sun_doodle.create_oval(
    sun_center[0] - sun_radius,
    sun_center[1] - sun_radius,
    sun_center[0] + sun_radius,
    sun_center[1] + sun_radius,
    fill=PINK,
    outline=PEACH,
    width=2,
)
sun_doodle.create_line(
    42, 51, 45, 54, 48, 51,
    fill=INK,
    width=2,
    smooth=True,
    capstyle=tk.ROUND,
)
sun_doodle.create_line(
    58, 51, 61, 54, 64, 51,
    fill=INK,
    width=2,
    smooth=True,
    capstyle=tk.ROUND,
)
sun_doodle.create_arc(
    46, 53, 60, 65,
    start=205,
    extent=130,
    style=tk.ARC,
    outline=INK,
    width=2,
)
sun_doodle.create_line(
    80, 19, 82, 25, 88, 27, 82, 29, 80, 35, 78, 29, 72, 27, 78, 25,
    fill=PETAL,
    width=1,
    smooth=True,
)
sun_doodle.create_line(
    22, 75, 24, 80, 29, 82, 24, 84, 22, 89, 20, 84, 15, 82, 20, 80,
    fill=PEACH,
    width=1,
    smooth=True,
)

filter_row = tk.Frame(shell, bg=BACKGROUND)
filter_row.pack(fill="x", pady=(15, 11))
tk.Label(
    filter_row,
    text="Screen filter",
    font=("Segoe UI", 11, "bold"),
    fg=INK,
    bg=BACKGROUND,
).pack(side="left")
toggle_button = tk.Button(
    filter_row,
    text="FILTER ON",
    command=toggle_filter,
    font=("Segoe UI", 9, "bold"),
    fg="#FFFFFF",
    bg=INK,
    activeforeground="#FFFFFF",
    activebackground=PURPLE,
    relief="flat",
    bd=0,
    padx=15,
    pady=7,
    cursor="hand2",
)
toggle_button.pack(side="right")

temperature_card = tk.Frame(shell, bg=CARD, padx=16, pady=12)
temperature_card.pack(fill="x", pady=(0, 10))
temperature_heading = tk.Frame(temperature_card, bg=CARD)
temperature_heading.pack(fill="x")
tk.Label(
    temperature_heading,
    text="COLOUR TEMPERATURE",
    font=("Segoe UI", 9, "bold"),
    fg=INK,
    bg=CARD,
).pack(side="left")
tk.Label(
    temperature_heading,
    textvariable=temperature_value,
    font=("Segoe UI", 12, "bold"),
    fg=INK,
    bg=CARD,
).pack(side="right")
tk.Scale(
    temperature_card,
    from_=1900,
    to=6500,
    resolution=100,
    orient="horizontal",
    variable=temp,
    command=apply,
    showvalue=False,
    length=360,
    sliderlength=20,
    width=14,
    bd=0,
    highlightthickness=0,
    bg=CARD,
    fg=INK,
    troughcolor=TRACK,
    activebackground=PINK,
).pack(fill="x", pady=(5, 0))
temperature_ends = tk.Frame(temperature_card, bg=CARD)
temperature_ends.pack(fill="x")
tk.Label(
    temperature_ends,
    text="Warmer",
    font=("Segoe UI", 9),
    fg=MUTED,
    bg=CARD,
).pack(side="left")
tk.Label(
    temperature_ends,
    text="Cooler",
    font=("Segoe UI", 9),
    fg=MUTED,
    bg=CARD,
).pack(side="right")

dimming_card = tk.Frame(shell, bg=CARD, padx=16, pady=12)
dimming_card.pack(fill="x", pady=(0, 13))
dimming_heading = tk.Frame(dimming_card, bg=CARD)
dimming_heading.pack(fill="x")
tk.Label(
    dimming_heading,
    text="SCREEN DIMMING",
    font=("Segoe UI", 9, "bold"),
    fg=INK,
    bg=CARD,
).pack(side="left")
tk.Label(
    dimming_heading,
    textvariable=dim_value,
    font=("Segoe UI", 12, "bold"),
    fg=INK,
    bg=CARD,
).pack(side="right")
tk.Scale(
    dimming_card,
    from_=0,
    to=50,
    orient="horizontal",
    variable=dim,
    command=apply,
    showvalue=False,
    length=360,
    sliderlength=20,
    width=14,
    bd=0,
    highlightthickness=0,
    bg=CARD,
    fg=INK,
    troughcolor=TRACK,
    activebackground=PINK,
).pack(fill="x", pady=(5, 0))
tk.Label(
    dimming_card,
    text="No dimming",
    font=("Segoe UI", 9),
    fg=MUTED,
    bg=CARD,
).pack(anchor="w")

tk.Label(
    shell,
    text="QUICK PRESETS",
    font=("Segoe UI", 9, "bold"),
    fg=INK,
    bg=BACKGROUND,
).pack(anchor="w", pady=(1, 7))
preset_row = tk.Frame(shell, bg=BACKGROUND)
preset_row.pack(fill="x")
for name, temperature, dimming in (
    ("Reading", 5200, 0),
    ("Evening", 3600, 10),
    ("Night", 2400, 25),
):
    tk.Button(
        preset_row,
        text=name,
        command=lambda t=temperature, d=dimming: preset(t, d),
        font=("Segoe UI", 10, "bold"),
        fg="#FFFFFF",
        bg=INK,
        activeforeground="#FFFFFF",
        activebackground=PURPLE,
        relief="flat",
        bd=0,
        padx=18,
        pady=9,
        cursor="hand2",
    ).pack(side="left", expand=True, fill="x", padx=(0, 7))

status_card = tk.Frame(shell, bg=STATUS_BACKGROUND, padx=12, pady=10)
status_card.pack(fill="x", pady=(14, 0))
status_label = tk.Label(
    status_card,
    textvariable=status,
    font=("Segoe UI", 9),
    fg=INK,
    bg=STATUS_BACKGROUND,
    wraplength=370,
    justify="left",
)
status_label.pack(anchor="w")

root.protocol("WM_DELETE_WINDOW", lambda: (reset(), root.destroy()))
apply()
root.mainloop()
