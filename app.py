import ctypes
import atexit
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
        s = max(MIN_SCALE, min(1.0, scales[ch]))
        for i in range(256):
            ramp[ch][i] = int(i * 257 * s)
    hdc = user32.GetDC(None)
    ok = gdi32.SetDeviceGammaRamp(hdc, ctypes.byref(ramp))
    user32.ReleaseDC(None, hdc)
    return bool(ok)


def reset():
    set_ramp((1.0, 1.0, 1.0))


atexit.register(reset)

root = tk.Tk()
root.title("BLUE LIGHT FILTER")
root.geometry("340x360")
root.resizable(False, False)

temp = tk.IntVar(value=3600)
dim = tk.IntVar(value=0)
enabled = tk.BooleanVar(value=True)
status = tk.StringVar()


def apply(*_):
    if not enabled.get():
        reset()
        status.set("Filter off")
        return
    r, g, b = kelvin_to_rgb(temp.get())
    d = 1 - dim.get() / 100
    ok = set_ramp((r * d, g * d, b * d))
    status.set(f"{temp.get()} K, dim {dim.get()}%" if ok
               else "Windows rejected this setting. Try a higher temperature.")


def preset(t, d):
    temp.set(t)
    dim.set(d)
    enabled.set(True)
    apply()


pad = {"padx": 16, "pady": 6}
tk.Label(root, text="BLUE LIGHT FILTER", font=("Georgia", 22)).pack(anchor="w", **pad)
tk.Checkbutton(root, text="Filter on", variable=enabled, command=apply).pack(anchor="w", **pad)
tk.Label(root, text="Colour temperature (K)").pack(anchor="w", padx=16)
tk.Scale(root, from_=1900, to=6500, resolution=100, orient="horizontal",
         variable=temp, command=apply, length=300).pack(**pad)
tk.Label(root, text="Dimming (%)").pack(anchor="w", padx=16)
tk.Scale(root, from_=0, to=50, orient="horizontal",
         variable=dim, command=apply, length=300).pack(**pad)

row = tk.Frame(root)
row.pack(**pad)
for name, t, d in (("Reading", 5200, 0), ("Evening", 3600, 10), ("Night", 2400, 25)):
    tk.Button(row, text=name, command=lambda t=t, d=d: preset(t, d)).pack(side="left", padx=4)

tk.Label(root, textvariable=status, fg="#666").pack(pady=8)
root.protocol("WM_DELETE_WINDOW", lambda: (reset(), root.destroy()))
apply()
root.mainloop()