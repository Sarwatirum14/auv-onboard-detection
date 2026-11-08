# Operating procedure (reproduces every number of the paper)

1. Data. Download URPC2020 (4 classes; 814 validation images) and RUOD (github.com/dlut-dimt/RUOD).
   Upload both as private Kaggle datasets. Validation images are processed in alphabetical order.
2. Detector. Fine-tune YOLOv8-n for 50 epochs at 640 px, batch 16, SGD, seed 42, deterministic=True
   (Cell 5). Seeds 43 and 44 are trained in session B for the training-seed study.
3. Detection cache. Run the detector once per image with confidence 0.1 and NMS IoU 0.45, after
   20 warm-up images; store boxes, scores, classes, latency and JPEG sizes (Cell 9).
4. Descriptor encoding. Quantize to Q_POS = 1024, Q_CONF = 255; bit-pack
   (50 bit/detection) and group into 64-byte payloads (Cell 7).
5. Channel. Frame error rate from Es/N0 (BPSK, 576-bit frames);
   iid erasure and Gilbert-Elliott bursts (Cell 8). Seeds [42, 43, 44, 45, 46]; report mean and standard deviation.
6. Baselines. JPEG q25/50/75 (with and without ARQ), JSCC autoencoder, DeepJSCC, split computing (Cells 11-21).
7. Link emulation. Send the real frames through the software-in-the-loop emulator at the datasheet frame timing,
   with bit errors and CRC-32 checking (Cell 25).
8. Physical layer and coverage. Thorp absorption, ambient noise and practical spreading, calibrated to the
   EvoLogics S2C R 18/34 power-range datasheet values; coverage maps and multi-AUV capacity (Cell 24).
9. Cost and energy. Energy per delivered image and 3-year TCO per scheme from datasheet values (Cell 23).
10. Release. run_config.json, requirements_frozen.txt, weights and all CSV files are archived in rev4_release.zip;
    publish on GitHub with a Zenodo DOI and cite the DOI in the paper (Cell 30).
