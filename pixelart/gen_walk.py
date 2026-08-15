#!/usr/bin/env python3
"""Generate a 6-frame front-view walk (dribble) for the Lakers player -> walk.json"""
import json

PALETTE = {
    ".": None, "K": "#241033", "H": "#15151f",
    "s": "#d29156", "h": "#e8b483", "d": "#a86a38",
    "P": "#5e2c8a", "p": "#3f1d63", "L": "#8148b0",
    "G": "#ffcf3f", "g": "#d19a1e",
    "W": "#eef0f5", "w": "#aab0c0",
    "B": "#e37b28", "b": "#b0551a"
}

W = 24

def pad(s):
    return s.ljust(W, ".")

# upper body (head + torso), rows 0..18. bob shifts it down 0 or 1 px.
UPPER = [
    "........KKKKKK",
    ".......KHHHHHHK",
    ".......KHHHHHHK",
    ".......KHssssHK",
    ".......KsKssKsK",
    ".......KssssssK",
    ".......KssddssK",
    "........KssssK",
    ".....KKKKKKKKKKKK",
    ".....KsKPPPGGPPPKsK",
    ".....KsKLPPGGPPLKsK",
    ".....KsKPPPGGPPPKsK",
    ".....KsKPPPGGPPPKsK",
    ".....KsKLPPPPPPLKsK",
    ".....KhKPPPPPPPPKhK",
    ".......KpGGGGGGpK",
    ".......KGGGGGGGGK",
    ".......KPPPPPPPPK",
    ".......KPPPPPPPPK",
]

# Leg poses. Each returns rows for y=19..29 (11 rows). Front view.
# "planted" leg = full length; "lifted" leg = raised 2px (foot up, shorter).
# left leg cols7-10, right leg cols12-15, gap col11.

def leg_rows(left="mid", right="mid"):
    """left/right in {'fwd','back','mid'}: fwd=planted low, back=lifted, mid=neutral."""
    # per-leg column-strings for a full stack of 11 rows (y19..y29)
    def stack(state):
        # returns list of 11 strings width4 (the leg block), plus x-offset for spread
        if state == "mid":
            return ["KPPK","KssK","KssK","KssK","KssK","KWWK","KWWK","KWWK","KWWK","KwwK","KKKK"], 0
        if state == "fwd":  # planted, slightly spread out & down
            return ["KPPK","KssK","KssK","KssK","KssK","KssK","KWWK","KWWK","KWWK","KwwK","KKKK"], 0
        if state == "back": # lifted: raise 2px, top transparent-ish, shorter
            return ["KPPK","KssK","KssK","KssK","KWWK","KWWK","KwwK","KKKK","....","....","...."], 0
        raise ValueError(state)
    L, lo = stack(left)
    R, ro = stack(right)
    rows = []
    for i in range(11):
        lcol = L[i]
        rcol = R[i]
        # left leg base col7, right leg base col12 (gap col11)
        row = "." * 7 + lcol + "." + rcol
        rows.append(row)
    return rows

# ball: 5x5, dark-lined. top-left corner at (bx, by).
BALL = [
    ".BBB.",
    "BBbBB",
    "BbBbB",
    "BBbBB",
    ".BBB.",
]

def place_ball(grid, bx, by):
    # grid is list of char-lists (mutable), width W. extend rows if needed.
    for j, brow in enumerate(BALL):
        y = by + j
        while len(grid) <= y:
            grid.append(list("." * W))
        for k, ch in enumerate(brow):
            if ch == ".":
                continue
            x = bx + k
            if 0 <= x < W:
                grid[y][x] = ch

def build_frame(bob, left, right, ball_y):
    rows = []
    if bob:
        rows.append("." * W)  # push everything down 1px
    for r in UPPER:
        rows.append(pad(r))
    for r in leg_rows(left, right):
        rows.append(pad(r))
    # normalize to char lists
    grid = [list(r.ljust(W, ".")) for r in rows]
    # dribble ball on right side, col 17
    place_ball(grid, 17, ball_y)
    # trim to consistent height 31
    out = ["".join(g) for g in grid]
    return out

# 6 frames: alternate stride, body bob on passing frames, ball bounces.
# stride: (left,right). ball_y: hand~14 (high) down to ~24 (low near ground).
FRAMES = [
    build_frame(0, "fwd",  "back", 15),  # L forward, ball leaving hand high
    build_frame(1, "mid",  "mid",  19),  # passing, bob up, ball mid-down
    build_frame(0, "back", "fwd",  24),  # R forward, ball low (bounce)
    build_frame(0, "fwd",  "back", 24),  # L forward, ball still low bouncing
    build_frame(1, "mid",  "mid",  19),  # passing, bob up, ball mid-up
    build_frame(0, "back", "fwd",  15),  # R forward, ball back to hand high
]

doc = {"palette": PALETTE, "scale": 12, "fps": 9, "frames": FRAMES}
json.dump(doc, open("walk.json", "w"), indent=0)
print("wrote walk.json", len(FRAMES), "frames")
