# Onboard Object Detection with Compact Descriptor Transmission for AUV Monitoring

Code and results for the paper on onboard object detection and fixed-point descriptor transmission over
bandwidth-constrained underwater acoustic links. A YOLOv8-n detector runs on the AUV and only compact,
bit-packed detection descriptors are sent to the surface station instead of images.

## Contents

| Path | Description |
| --- | --- |
| `auv_onboard_detection.ipynb` | Complete experiment notebook (Kaggle, T4 GPU) |
| `results/session_A/` | Channel experiments, baselines, energy, coverage, link emulation |
| `results/session_BC/` | Detector training seeds and RUOD cross-dataset evaluation |
| `results/session_Q/` | Quantization, confidence threshold and JPEG quality ablations |
| `requirements.txt` | Python packages |

Each results folder contains the CSV tables, figures, `parameter_table.csv`/`.tex`, `operating_procedure.md`,
`run_config.json` and `requirements_frozen.txt` of that run. The trained detector is
`results/session_A/rev4_release/yolov8n_urpc_best.pt`.

## Datasets

The datasets are not redistributed here.

- URPC2020 (4 classes), in YOLO format with `data.yaml`, `train/` and `valid/`
- RUOD (10 classes): https://github.com/dlut-dimt/RUOD

## How to run

1. Create a Kaggle notebook from `auv_onboard_detection.ipynb` with a T4 GPU and internet enabled.
2. Add URPC2020 as an input. To reuse the trained detector, also add `yolov8n_urpc_best.pt`; otherwise
   Cell 5 trains YOLOv8-n with seed 42 (about 1.5 h).
3. Set `SESSION` in Cell 3 and run all cells.

| Session | Content | Time on a T4 |
| --- | --- | --- |
| `A` | Channel experiments, baselines, energy, coverage, link emulation | 4 to 5 h |
| `B` | Detector training seeds 43 and 44 | 3 h |
| `C` | RUOD evaluation and quantization ablations (add RUOD as an input) | 2 h |
| `Q` | Quantization, confidence threshold and JPEG quality ablations | 15 min |
| `D` | JSCC at 640 x 640 (optional) | 2 to 3 h |

Outputs are written to `/kaggle/working/results` and packed into a zip by Cell 30.

## Main results (URPC2020, 10 % frame loss, mean ± std over 5 seeds)

| Method | mAP@0.5 | Data per image | Frame rate at 10 kbit/s |
| --- | --- | --- | --- |
| Proposed, bit-packed descriptors | 0.6886 ± 0.0035 | 0.67 kbit | 6.8 fps |
| JPEG q50 with selective repeat ARQ | 0.6459 | 81.8 kbit | 0.058 fps |

- Energy per delivered image: 1.31 J (proposed) vs 48.4 J (JPEG with ARQ).
- Three detector training seeds: oracle mAP@0.5 0.7711 ± 0.0043.
- RUOD: 0.7172 ± 0.0024 at 10 % frame loss (oracle 0.7953).

## License

MIT, see `LICENSE`.
