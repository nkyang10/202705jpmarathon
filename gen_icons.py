#!/usr/bin/env python3
"""Generate 9 flat-illustration clipart icons via remote ComfyUI z_image_turbo."""
import json, time, urllib.request, urllib.parse, os, sys

BASE = "http://192.168.1.162:8000"
OUTDIR = "/home/ubuntu/202705jpmarathon/assets/icons"

# Shared style suffix for consistent flat vector clipart look
STYLE = (
    "modern flat vector illustration clipart icon, bold clean geometric shapes, "
    "smooth edges, vibrant cheerful colors, coral orange, sunny yellow, sky blue, "
    "grass green, plain solid white background, centered composition, full body, "
    "no text, no words, no letters, no watermark, no signature, not photorealistic, "
    "not a photograph, not a sketch, clean minimal design, high contrast"
)

# Descriptions by filename
ICONS = {
    "icon-runner.png": "dynamic marathon runner in motion, mid-stride running pose, energetic, arms swinging, motion lines behind",
    "icon-medal.png": "gold finish medal with red blue ribbon, celebration, shiny golden circle with star",
    "icon-guarantee.png": "round stamp ticket with green checkmark symbol, guaranteed entry badge, certificate seal",
    "icon-sakura.png": "pink cherry blossom flower with five petals, spring sakura, small yellow center, two leaves",
    "icon-train.png": "Japan shinkansen bullet train, front angled three-quarter view, sleek white blue nose, single headlight",
    "icon-pb.png": "rising arrow and speedometer gauge going up, personal best performance, upward graph arrow and dashboard",
    "icon-onsen.png": "hot spring onsen pool with rising steam curls, wooden bucket beside, snowy mountain in background, relaxed",
    "icon-gyutan.png": "grilled beef skewers gyutan on a round plate, tasty BBQ meat skewers, char marks, on grilled grill",
    "icon-friends.png": "three happy runners running together as friends, three running figures in a row, joyful",
}


def api_free():
    try:
        req = urllib.request.Request(f"{BASE}/api/free", data=b"{}",
                                     headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=20)
        print("called /api/free")
    except Exception as e:
        print("free warn:", e)


def download(url, path):
    data = urllib.request.urlopen(url, timeout=120).read()
    with open(path, "wb") as f:
        f.write(data)
    return len(data)


def build_workflow(prompt, width=1024, height=1024, seed=None):
    if seed is None:
        seed = int(time.time() * 1000) % 2_000_000_000
    return {
        # UNETLoader
        "1": {"class_type": "UNETLoader", "inputs": {
            "unet_name": "z_image_turbo_bf16.safetensors", "weight_dtype": "default"}},
        # CLIPLoader
        "10": {"class_type": "CLIPLoader", "inputs": {
            "clip_name": "qwen_3_4b.safetensors", "type": "lumina2", "device": "default"}},
        # VAELoader
        "9": {"class_type": "VAELoader", "inputs": {"vae_name": "ae.safetensors"}},
        # positive conditioning
        "2": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["10", 0]}},
        # negative -> zero out
        "3": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["2", 0]}},
        # latent
        "4": {"class_type": "EmptySD3LatentImage", "inputs": {
            "width": width, "height": height, "batch_size": 1}},
        # sampling shift
        "12": {"class_type": "ModelSamplingAuraFlow", "inputs": {
            "shift": 3, "model": ["1", 0]}},
        # sampler
        "5": {"class_type": "KSampler", "inputs": {
            "seed": seed, "steps": 8, "cfg": 1.0, "sampler_name": "res_multistep",
            "scheduler": "simple", "denoise": 1.0, "model": ["12", 0],
            "positive": ["2", 0], "negative": ["3", 0], "latent_image": ["4", 0]}},
        # decode
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["9", 0]}},
        # save
        "11": {"class_type": "SaveImage", "inputs": {
            "images": ["8", 0], "filename_prefix": "icon_gen"}},
    }


def queue(prompt, width, height, seed):
    wf = build_workflow(prompt, width, height, seed)
    data = json.dumps({"prompt": wf}).encode()
    req = urllib.request.Request(f"{BASE}/prompt", data=data,
                                 headers={"Content-Type": "application/json"})
    resp = urllib.request.urlopen(req, timeout=60)
    result = json.loads(resp.read())
    return result["prompt_id"]


def poll(prompt_id, timeout=180):
    for _ in range(timeout):
        try:
            resp = urllib.request.urlopen(f"{BASE}/history/{prompt_id}", timeout=20)
            hist = json.loads(resp.read())
            if str(prompt_id) in hist:
                return hist[str(prompt_id)]
        except Exception:
            pass
        time.sleep(1)
    return None


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    # free GPU before starting z_image_turbo family
    api_free()
    results = []
    for fname, desc in ICONS.items():
        prompt = f"{desc}, {STYLE}"
        opath = os.path.join(OUTDIR, fname)
        if os.path.exists(opath) and os.path.getsize(opath) > 0:
            sz = os.path.getsize(opath)
            results.append((fname, opath, sz, "exists-skip"))
            print(f"[skip existing] {fname} ({sz}B)")
            continue
        try:
            pid = queue(prompt, 1024, 1024, None)
            print(f"[gen] {fname} queued {pid}")
            hist = poll(pid)
            if hist is None:
                results.append((fname, None, 0, "timeout"))
                print(f"[FAIL timeout] {fname}")
                continue
            outputs = hist.get("outputs", {})
            img = None
            for node_id, out in outputs.items():
                if "images" in out and out["images"]:
                    img = out["images"][0]
                    break
            if img is None:
                results.append((fname, None, 0, "no-image-output"))
                print(f"[FAIL no output] {fname}")
                continue
            fn = img["filename"]
            subfolder = img.get("subfolder", "")
            url = f"{BASE}/view?filename={urllib.parse.quote(fn)}&subfolder={urllib.parse.quote(subfolder)}&type=output"
            sz = download(url, opath)
            results.append((fname, opath, sz, "generated"))
            print(f"[done] {fname} -> {sz}B")
        except Exception as e:
            results.append((fname, None, 0, f"error:{e}"))
            print(f"[FAIL error] {fname}: {e}")

    print("\n===== SUMMARY =====")
    for fname, path, sz, st in results:
        print(f"{fname}\t{sz}B\t{st}\t{path}")


if __name__ == "__main__":
    main()
