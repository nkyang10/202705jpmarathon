#!/bin/bash
# CM scene renders via ComfyUI MiniMax H3 I2V
cd /home/ubuntu
H3=/home/ubuntu/.hermes/skills/video-production/comfyui-video-pipeline/scripts/h3_i2v.py
IMG=/home/ubuntu/202705jpmarathon/assets
V=/home/ubuntu/202705jpmarathon/video

echo "=== scene 1: 仙台晨光 ==="
python3 $H3 $IMG/hero-sendai.jpg 202705jpmarathon/video/scenes/s1 $V/prompts/s1.txt --width 832 --height 480 --frames 124 --seed 101
echo "=== scene 2: 半馬起跑 ==="
python3 $H3 $IMG/hero-sendai.jpg 202705jpmarathon/video/scenes/s2 $V/prompts/s2.txt --width 832 --height 480 --frames 124 --seed 202
echo "=== scene 3: 松島 ==="
python3 $H3 $IMG/matsushima.jpg 202705jpmarathon/video/scenes/s3 $V/prompts/s3.txt --width 832 --height 480 --frames 124 --seed 303
echo "=== scene 4: 溫泉 ==="
python3 $H3 $IMG/onsen.jpg 202705jpmarathon/video/scenes/s4 $V/prompts/s4.txt --width 832 --height 480 --frames 124 --seed 404
echo "=== scene 5: 奥州全馬 ==="
python3 $H3 $IMG/oshumarathon.jpg 202705jpmarathon/video/scenes/s5 $V/prompts/s5.txt --width 832 --height 480 --frames 124 --seed 505
echo "=== scene 6: 品牌卡 ==="
python3 $H3 $V/endcard.png 202705jpmarathon/video/scenes/s6 $V/prompts/s6.txt --width 832 --height 480 --frames 124 --seed 606

echo "=== ALL SCENES DONE ==="
ls -la $V/scenes/*.mp4 2>/dev/null
# release H3 from VRAM
curl -s -X POST http://192.168.1.162:8000/free -H "Content-Type: application/json" -d '{"unload_models":true,"free_memory":true}'
echo "H3 released"
