#!/usr/bin/env python3
"""Build the new 30s CM: 10 x 3s clips, xfade movie transitions, bottom-right captions,
ambient audio + Cantonese voiceover. Run AFTER all 10 scene clips exist."""
import os, subprocess, sys

V = "/home/ubuntu/202705jpmarathon/video"
S = f"{V}/scenes"
C = f"{V}/captions"
VO = f"{V}/voice"
OUT = f"{V}/CM-東北雙馬拉松2027-v2.mp4"

# order: clip, caption, (voice line to start here if any)
plan = [
    ("s1.mp4",  "cap01.png", "s1.mp3"),
    ("s2.mp4",  "cap02.png", "s2.mp3"),
    ("s10.mp4", "cap03.png", None),
    ("s7.mp4",  "cap04.png", "s3.mp3"),
    ("s3.mp4",  "cap05.png", None),
    ("s4.mp4",  "cap06.png", "s4.mp3"),
    ("s8.mp4",  "cap07.png", None),
    ("s5.mp4",  "cap08.png", "s5.mp3"),
    ("s9.mp4",  "cap09.png", None),
    ("s6.mp4",  "cap10.png", "s6.mp3"),
]
N = len(plan)
DUR = 3.0    # per clip
FD = 0.4     # crossfade
# total = N*DUR - (N-1)*FD
total = N * DUR - (N - 1) * FD
STEP = DUR - FD  # 2.6

# offsets for xfade
xfade_offsets = [STEP * i for i in range(1, N)]  # between clip i and i+1 (0-indexed i)

parts = []

# --- trim inputs ---
for i in range(N):
    clip = plan[i][0]
    parts.append(f"[{i}:v]trim=duration={DUR},setpts=PTS-STARTPTS,scale=832:480[v{i}];")

# --- xfade chain ---
prev = "v0"
for i in range(1, N):
    out = f"xf{i}"
    parts.append(f"[{prev}][v{i}]xfade=transition=fade:duration={FD}:offset={xfade_offsets[i-1]:.2f}[{out}];")
    prev = out

# --- caption overlays (inputs 10..19 are the caption PNGs) ---
prev = out
for i in range(N):
    out = f"c{i}"
    start = i * STEP
    end = start + DUR - 0.2
    parts.append(f"[{prev}][{10+i}:v]overlay=0:0:enable='between(t,{start:.2f},{end:.2f})'[{out}];")
    prev = out
vid = out

# --- audio: ambient (concat with acrossfade) ---
# trim each clip audio to DUR
for i in range(N):
    parts.append(f"[{i}:a]atrim=0:{DUR},asetpts=PTS-STARTPTS[a{i}];")
# acrossfade chain
aprev = "a0"
for i in range(1, N):
    aout = f"ax{i}"
    parts.append(f"[{aprev}][a{i}]acrossfade=d={FD}[{aout}];")
    aprev = aout
parts.append(f"[{aprev}]volume=0.42[amb];")

# --- voiceover mix (voice mp3s are inputs 20..25) ---
v_in = 0
for i, (clip, cap, voice) in enumerate(plan):
    if voice:
        parts.append(f"[{20+v_in}:a]adelay={int(i*STEP*1000)}:all=1[vo{v_in}];")
        v_in += 1
# combine voiceover parts
vo_parts = [f"[vo{i}]" for i in range(v_in)]
if vo_parts:
    if v_in == 1:
        parts.append(f"{vo_parts[0]}volume=1.1[vomix];")
    else:
        parts.append(f"{''.join(vo_parts)}amix=inputs={v_in}:normalize=0,volume=1.1[vomix];")
    # final audio
    parts.append(f"[amb][vomix]amix=inputs=2:duration=first:weights='1 1'[outa];")
else:
    parts.append(f"[amb]anull[outa];")

# fades
parts.append(f"[{vid}]fade=t=in:d=0.4,fade=t=out:st={total-0.8:.2f}:d=0.8[vfin];")
parts.append(f"[outa]afade=t=in:d=0.3,afade=t=out:st={total-0.8:.2f}:d=0.8[afin];")

filter_complex = "".join(parts)

# inputs: 10 videos + 10 captions + voice mp3s (0..5)
cmd = ["ffmpeg", "-y"]
for clip, cap, voice in plan:
    cmd += ["-i", f"{S}/{clip}"]
for clip, cap, voice in plan:
    cmd += ["-i", f"{C}/{cap}"]
for clip, cap, voice in plan:
    if voice:
        cmd += ["-i", f"{VO}/{voice}"]
cmd += ["-filter_complex", filter_complex,
        "-map", "[vfin]", "-map", "[afin]",
        "-c:v", "libx264", "-crf", "18", "-preset", "medium",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
        "-t", f"{total:.2f}", OUT]

print("filter_complex length:", len(filter_complex))
print("total duration:", round(total,2))
print("running ffmpeg...")
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print("FFMPEG ERROR:\n", r.stderr[-3000:])
    sys.exit(1)
print("OK ->", OUT)
