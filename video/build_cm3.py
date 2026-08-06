#!/usr/bin/env python3
"""Build CM v3: 10 scenes, varied dramatic xfade transitions, bottom-right captions,
balanced scene mix (fewer running scenes), explicit 16:9 SAR. Run after all scenes exist."""
import os, subprocess, sys

V = "/home/ubuntu/202705jpmarathon/video"
S = f"{V}/scenes"; C = f"{V}/captions"; VO = f"{V}/voice"
OUT = f"{V}/CM-東北雙馬拉松2027-v3.mp4"

# clip, caption, voice-line-at-this-scene(if any)
plan = [
    ("s1.mp4",  "cap01.png", "s1.mp3"),   # 仙台晨光
    ("s2.mp4",  "cap02.png", "s2.mp3"),   # 半馬
    ("s7.mp4",  "cap03.png", "s3.mp3"),   # 平泉
    ("s11.mp4", "cap04.png", None),       # 嚴美溪
    ("s3.mp4",  "cap05.png", None),       # 松島
    ("s12.mp4", "cap06.png", None),       # 秋保瀑布
    ("s8.mp4",  "cap07.png", "s4.mp3"),   # 牛舌
    ("s4.mp4",  "cap08.png", None),       # 溫泉
    ("s5.mp4",  "cap09.png", "s5.mp3"),   # 奥州全馬
    ("s6.mp4",  "cap10.png", "s6.mp3"),   # 品牌
]
# varied dramatic movie-style transitions (ffmpeg xfade) per cut
transitions = ["slideleft", "fadeblack", "circleopen", "dissolve", "diagtr",
               "pixelize", "radial", "coverleft", "zoomin"]
N = len(plan)
DUR = 3.0
FD = 0.45
# xfade offset for cut i = i*(DUR-FD)
STEP = DUR - FD  # 2.55
total = N*DUR - (N-1)*FD

parts = []
for i in range(N):
    parts.append(f"[{i}:v]trim=duration={DUR},setpts=PTS-STARTPTS,scale=832:480,setsar=1[v{i}];")

prev = "v0"
for i in range(1, N):
    out = f"xf{i}"
    t = transitions[i-1]
    off = i * STEP
    parts.append(f"[{prev}][v{i}]xfade=transition={t}:duration={FD}:offset={off:.2f}[{out}];")
    prev = out

prev = out
for i in range(N):
    out = f"c{i}"
    start = i*STEP; end = start + DUR - 0.15
    parts.append(f"[{prev}][{10+i}:v]overlay=0:0:enable='between(t,{start:.2f},{end:.2f})'[{out}];")
    prev = out
vid = out

# audio ambient (acrossfade chain)
for i in range(N):
    parts.append(f"[{i}:a]atrim=0:{DUR},asetpts=PTS-STARTPTS[a{i}];")
aprev = "a0"
for i in range(1, N):
    aout = f"ax{i}"
    parts.append(f"[{aprev}][a{i}]acrossfade=d={FD}[{aout}];")
    aprev = aout
parts.append(f"[{aprev}]volume=0.42[amb];")

# voiceover (inputs 20..25)
v_in = 0
for i, (clip, cap, voice) in enumerate(plan):
    if voice:
        parts.append(f"[{20+v_in}:a]adelay={int(i*STEP*1000)}:all=1[vo{v_in}];")
        v_in += 1
if v_in:
    if v_in == 1:
        parts.append("[vo0]volume=1.1[vomix];")
    else:
        parts.append(f"{''.join(f'[vo{j}]' for j in range(v_in))}amix=inputs={v_in}:normalize=0,volume=1.1[vomix];")
    parts.append("[amb][vomix]amix=inputs=2:duration=first:weights='1 1'[outa];")
else:
    parts.append("[amb]anull[outa];")

parts.append(f"[{vid}]fade=t=in:d=0.4,fade=t=out:st={total-0.8:.2f}:d=0.8[vfin];")
parts.append(f"[outa]afade=t=in:d=0.3,afade=t=out:st={total-0.8:.2f}:d=0.8[afin];")

fc = "".join(parts)
cmd = ["ffmpeg", "-y"]
for clip, cap, voice in plan:
    cmd += ["-i", f"{S}/{clip}"]
for clip, cap, voice in plan:
    cmd += ["-i", f"{C}/{cap}"]
for clip, cap, voice in plan:
    if voice:
        cmd += ["-i", f"{VO}/{voice}"]
cmd += ["-filter_complex", fc, "-map", "[vfin]", "-map", "[afin]",
        "-c:v", "libx264", "-crf", "18", "-preset", "medium",
        "-c:a", "aac", "-b:a", "192k", "-aspect", "16:9", "-movflags", "+faststart",
        "-t", f"{total:.2f}", OUT]
print("total:", round(total,2), "| transitions:", transitions)
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print("FFMPEG ERROR:\n", r.stderr[-2500:]); sys.exit(1)
print("OK ->", OUT)
