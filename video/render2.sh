#!/bin/bash
# Additional CM scenes
cd /home/ubuntu
H3=/home/ubuntu/.hermes/skills/video-production/comfyui-video-pipeline/scripts/h3_i2v.py
IMG=/home/ubuntu/202705jpmarathon/assets
V=/home/ubuntu/202705jpmarathon/video
mkdir -p $V/prompts
echo "=== scene 7: 平泉金色堂 ===" > $V/render2.log
cat > $V/prompts/s7.txt <<'EOF'
金色堂緩慢推近，莊嚴寧靜，庭園新綠，陽光透入。音效：微風、鳥鳴
EOF
python3 $H3 $IMG/hiraizumi.jpg 202705jpmarathon/video/scenes/s7 $V/prompts/s7.txt --width 832 --height 480 --frames 81 --seed 707 >> $V/render2.log 2>&1
echo "=== scene 8: 牛舌 ===" >> $V/render2.log
cat > $V/prompts/s8.txt <<'EOF'
牛舌燒肉冒煙，鏡頭拉近，炭火滋滋，油光閃亮。音效：烤肉聲、滋滋聲
EOF
python3 $H3 $IMG/gyutan.jpg 202705jpmarathon/video/scenes/s8 $V/prompts/s8.txt --width 832 --height 480 --frames 81 --seed 808 >> $V/render2.log 2>&1
echo "=== scene 9: 冲線慶祝 ===" >> $V/render2.log
cat > $V/prompts/s9.txt <<'EOF'
跑手群沿田園賽道奔跑到終點，動態跟拍，慶祝氣氛，揮手。音效：跑步聲、歡呼聲
EOF
python3 $H3 $IMG/oshumarathon.jpg 202705jpmarathon/video/scenes/s9 $V/prompts/s9.txt --width 832 --height 480 --frames 81 --seed 909 >> $V/render2.log 2>&1
echo "=== scene 10: 跑手特寫 ===" >> $V/render2.log
cat > $V/prompts/s10.txt <<'EOF'
跑手特寫追蹤，呼吸起伏，朝氣，陽光。音效：呼吸聲、腳步聲
EOF
python3 $H3 $IMG/hero-sendai.jpg 202705jpmarathon/video/scenes/s10 $V/prompts/s10.txt --width 832 --height 480 --frames 81 --seed 1010 >> $V/render2.log 2>&1
echo "=== DONE ===" >> $V/render2.log
ls -la $V/scenes/s7.mp4 $V/scenes/s8.mp4 $V/scenes/s9.mp4 $V/scenes/s10.mp4 2>/dev/null >> $V/render2.log
curl -s -X POST http://192.168.1.162:8000/free -H "Content-Type: application/json" -d '{"unload_models":true,"free_memory":true}'
echo "H3 released" >> $V/render2.log
