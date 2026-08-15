#!/usr/bin/env python3
"""Render a sprite/anim grid to a flat PNG (checker bg) so it can be eyeballed."""
import json, sys
sys.path.insert(0, "/Users/angelesmoralesaguirre/.claude/skills/pixel-art-studio/scripts")
from render import norm_rows, color_of, hex_rgb
from PIL import Image

def cell_img(grid, palette, cell, checker=True):
    rows, w, h = norm_rows(grid)
    img = Image.new("RGB", (w*cell, h*cell), (40,40,48))
    px = img.load()
    if checker:
        for y in range(h*cell):
            for x in range(w*cell):
                if ((x//cell)+(y//cell)) % 2 == 0:
                    px[x,y] = (52,52,62)
    for y,row in enumerate(rows):
        for x in range(w):
            c = color_of(row[x], palette)
            if c is None: continue
            r,g,b = hex_rgb(c)
            for dy in range(cell):
                for dx in range(cell):
                    px[x*cell+dx, y*cell+dy] = (r,g,b)
    return img

def main():
    path, out = sys.argv[1], sys.argv[2]
    cell = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    s = json.load(open(path))
    pal = s["palette"]
    if "frames" in s:
        frames = s["frames"]
        imgs = [cell_img(f, pal, cell) for f in frames]
        w = max(i.width for i in imgs); h = max(i.height for i in imgs)
        sheet = Image.new("RGB", ((w+cell)*len(imgs), h), (24,24,30))
        for i,im in enumerate(imgs):
            sheet.paste(im, (i*(w+cell), 0))
        sheet.save(out)
    else:
        cell_img(s["pixels"], pal, cell).save(out)
    print("wrote", out)

main()
