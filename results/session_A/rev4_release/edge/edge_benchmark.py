
# On-device latency benchmark. Copy the edge folder to the device and run:
#   Raspberry Pi 5:  pip install ultralytics ncnn
#                    python edge_benchmark.py --weights best.pt --format ncnn
#   Jetson:          pip install ultralytics   (JetPack with TensorRT)
#                    python edge_benchmark.py --weights best.pt --format engine --tegrastats
# Power: on Jetson the script logs tegrastats. On the Pi read the inline USB meter during the run.
import argparse, glob, json, os, subprocess, time
import numpy as np
from ultralytics import YOLO

ap = argparse.ArgumentParser()
ap.add_argument("--weights", default="best.pt")
ap.add_argument("--format", default="ncnn", choices=["pt", "onnx", "ncnn", "engine"])
ap.add_argument("--imgsz", type=int, default=640)
ap.add_argument("--frames", type=int, default=300)
ap.add_argument("--tegrastats", action="store_true")
a = ap.parse_args()

model_path = a.weights
if a.format != "pt":
    kw = {"half": True} if a.format == "engine" else {}
    model_path = YOLO(a.weights).export(format=a.format, imgsz=a.imgsz, **kw)
model = YOLO(model_path, task="detect")
imgs = sorted(glob.glob("sample_images/*"))
proc = None
if a.tegrastats:
    log = open("tegrastats.log", "w")
    proc = subprocess.Popen(["tegrastats", "--interval", "100"], stdout=log)
for p in imgs[:20]:
    model(p, imgsz=a.imgsz, conf=0.10, iou=0.45, verbose=False)
lat = []
for k in range(a.frames):
    t0 = time.perf_counter()
    model(imgs[k % len(imgs)], imgsz=a.imgsz, conf=0.10, iou=0.45, verbose=False)
    lat.append((time.perf_counter() - t0) * 1000)
if proc:
    proc.terminate()
res = {"format": a.format, "imgsz": a.imgsz, "frames": a.frames,
       "latency_ms_mean": float(np.mean(lat)), "latency_ms_std": float(np.std(lat)),
       "latency_ms_p95": float(np.percentile(lat, 95)), "fps": float(1000 / np.mean(lat))}
if a.tegrastats and os.path.exists("tegrastats.log"):
    import re
    mw = [int(m.group(1)) for m in re.finditer(r"VDD_IN (\d+)mW", open("tegrastats.log").read())]
    if mw:
        res["power_w_mean"] = float(np.mean(mw) / 1000)
print(json.dumps(res, indent=2))
json.dump(res, open("edge_result.json", "w"), indent=2)
