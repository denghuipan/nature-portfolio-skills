"""Audit exported figure PDFs against Nature Portfolio artwork rules:
page size (89 or 183 mm wide, <= 170 mm tall), fonts (Arial family only), type sizes (5-7 pt body, 8 pt bold
panel letters), panel letters (lowercase, bold, order, offset from their axes frame), axes-frame alignment
(edges that are nearly but not exactly aligned), raster images (effective dpi), thin lines (< 0.25 pt),
text outside the page.

Run:  python scripts/audit_layout.py figure1.pdf [figure2.pdf ...]      (needs: pip install pymupdf)
Prints the report and writes <name>_audit.md next to each PDF.
"""
import collections
import pathlib
import sys

import pymupdf

PT = 25.4 / 72


def mm(v):
    return v * PT


def cluster(vals, tol):
    vals = sorted(vals)
    groups, cur = [], [vals[0]]
    for v in vals[1:]:
        if v - cur[-1] <= tol:
            cur.append(v)
        else:
            groups.append(cur); cur = [v]
    groups.append(cur)
    return groups


def audit(pdf):
    doc = pymupdf.open(pdf)
    page = doc[0]
    W, H = mm(page.rect.width), mm(page.rect.height)
    out = [f"# {pathlib.Path(pdf).parent.name}/{pathlib.Path(pdf).name}", f"- page: {W:.1f} x {H:.1f} mm"
           + ("" if abs(W - 183) < 0.3 or abs(W - 89) < 0.3 else "  **width not 183/89 mm**")
           + ("" if H <= 170.05 else "  **height > 170 mm**")]
    # ---- text
    spans = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            for s in l["spans"]:
                t = s["text"].strip()
                if t:
                    spans.append(dict(text=t, font=s["font"], size=s["size"], bbox=[mm(x) for x in s["bbox"]],
                                      bold="Bold" in s["font"] or (s["flags"] & 16) != 0))
    fonts = collections.Counter(s["font"] for s in spans)
    out.append("- fonts: " + ", ".join(f"{k} x{v}" for k, v in fonts.most_common()))
    nonarial = [k for k in fonts if "Arial" not in k and "Helvetica" not in k]
    if nonarial:
        out.append(f"  **non-Arial fonts: {nonarial}**")
    sizes = collections.Counter(round(s["size"], 1) for s in spans)
    out.append("- sizes (pt): " + ", ".join(f"{k} x{v}" for k, v in sorted(sizes.items())))
    letters = [s for s in spans if len(s["text"]) == 1 and s["text"].islower() and s["text"].isalpha() and s["bold"]
               and 7.5 <= s["size"] <= 8.5]
    odd = [s for s in spans if not (4.95 <= s["size"] <= 7.05) and s not in letters]
    if odd:
        out.append("- **type outside 5-7 pt (not a panel letter):** " + "; ".join(
            f"'{s['text'][:25]}' {s['size']:.1f} pt @({s['bbox'][0]:.0f},{s['bbox'][1]:.0f})" for s in odd[:12]))
    bold_other = [s for s in spans if s["bold"] and s not in letters]
    if bold_other:
        out.append("- bold text other than panel letters: " + "; ".join(f"'{s['text'][:25]}'" for s in bold_other[:10]))
    off = [s for s in spans if s["bbox"][0] < -0.05 or s["bbox"][2] > W + 0.05 or s["bbox"][1] < -0.05 or s["bbox"][3] > H + 0.05]
    if off:
        out.append("- **text outside the page:** " + "; ".join(f"'{s['text'][:25]}' {s['bbox']}" for s in off[:8]))
    # ---- axes frames: white filled rectangles (axes patches), not the page itself
    rects = []
    thin = []
    for d in page.get_drawings():
        r = d.get("rect")
        if d.get("fill") == (1.0, 1.0, 1.0) and r is not None and d.get("width") in (None, 0, 0.0) or (
                d.get("fill") == (1.0, 1.0, 1.0) and d.get("color") is None and r is not None):
            rm = [mm(r.x0), mm(r.y0), mm(r.x1), mm(r.y1)]
            w, h = rm[2] - rm[0], rm[3] - rm[1]
            if w * h > 15 and not (w > W - 1 and h > H - 1):
                rects.append(rm)
        if d.get("color") is not None and d.get("width") is not None and 0 < d["width"] < 0.25:
            thin.append(d["width"])
    # dedupe
    uniq = []
    for r in rects:
        if not any(all(abs(a - b) < 0.05 for a, b in zip(r, u)) for u in uniq):
            uniq.append(r)
    rects = sorted(uniq, key=lambda r: (round(r[1] / 5), r[0]))
    out.append(f"- axes frames (white patches): {len(rects)}")
    for r in rects:
        out.append(f"    [{r[0]:6.1f} {r[1]:6.1f} {r[2]:6.1f} {r[3]:6.1f}]  {r[2]-r[0]:5.1f} x {r[3]-r[1]:5.1f} mm")
    if thin:
        out.append(f"- lines thinner than 0.25 pt: {len(thin)} (min {min(thin):.2f} pt)")
    # ---- near-misses in alignment: edges within 1.2 mm of each other but not within 0.15 mm
    for name, idx in (("left", 0), ("right", 2), ("top", 1), ("bottom", 3)):
        vals = [r[idx] for r in rects]
        if len(vals) < 2:
            continue
        for g in cluster(vals, 1.2):
            if len(g) > 1 and max(g) - min(g) > 0.15:
                out.append(f"- **{name} edges nearly aligned (spread {max(g)-min(g):.2f} mm):** "
                           + ", ".join(f"{v:.2f}" for v in g))
    # ---- panel letters: position relative to the nearest frame (frame whose top-left is right/below the letter)
    letters.sort(key=lambda s: (round(s["bbox"][1] / 8), s["bbox"][0]))
    seq = "".join(s["text"] for s in letters)
    out.append(f"- panel letters: {seq}  ({len(letters)})" + ("" if seq == "".join(sorted(seq)) else "  **order?**"))
    for s in letters:
        x, y = s["bbox"][0], s["bbox"][1]
        cand = [r for r in rects if r[0] >= x - 1 and r[1] >= y - 1]
        if cand:
            r = min(cand, key=lambda r: (r[0] - x) + (r[1] - y))
            out.append(f"    {s['text']}: {s['size']:.1f} pt at ({x:.1f}, {y:.1f}); nearest frame dx {r[0]-x:.1f} dy {r[1]-y:.1f} mm")
        else:
            out.append(f"    {s['text']}: {s['size']:.1f} pt at ({x:.1f}, {y:.1f}); no frame to its lower right")
    # ---- images
    imgs = page.get_image_info(xrefs=True)
    if imgs:
        lines = []
        for im in imgs:
            bw, bh = mm(im["bbox"][2] - im["bbox"][0]), mm(im["bbox"][3] - im["bbox"][1])
            dpi = im["width"] / (bw / 25.4) if bw > 0 else 0
            lines.append(f"{im['width']}x{im['height']} px in {bw:.1f}x{bh:.1f} mm = {dpi:.0f} dpi")
        out.append(f"- raster images: {len(imgs)}: " + "; ".join(lines[:14]))
        low = [l for l in lines if float(l.split('= ')[1].split()[0]) < 300]
        if low:
            out.append(f"  **images below 300 dpi:** {len(low)}")
    return "\n".join(out)


if __name__ == "__main__":
    for pdf in sys.argv[1:]:
        rep = audit(pdf)
        pdf = pathlib.Path(pdf).resolve()
        (pdf.parent / (pdf.stem + "_audit.md")).write_text(rep)          # report next to the audited PDF
        print(rep)
        print()
