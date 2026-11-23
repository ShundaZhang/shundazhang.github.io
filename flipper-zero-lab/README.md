# Flipper Zero Hacking Lab

Bilingual static field guide, English by default with a Chinese edition. The personal homepage links to this topic under Security as entry 18.

## Build and test

```sh
python3 build.py
python3 check.py
```

Python standard library only. The build generates both HTML pages and the original bilingual SVG teaching diagrams. Official illustrations are stored locally with source-page and original-asset provenance in `assets/credits.json`; rights remain with their respective owners. This is a curated guide, not a mirror of community repositories.

## Practical downloads

- `downloads/pulse_inspect.py` — offline RAW timing statistics and SVG output
- `downloads/synthetic.sub` — synthetic timing input, not a captured credential or Nice frame
- `downloads/visible-hid.txt` — text-editor-only HID demonstration
- `downloads/lab-notebook.md` — bilingual experiment record
- `downloads/bit-lab-source.zip` — complete original Bit Lab source
- `downloads/bit_lab.fap` — compiled game, official release SDK 1.5.1, f7 target, API 88.2

Bit Lab compilation and the FAP package check passed with uFBT 0.2.6. Binary SHA256 is `dbf719577b29489d5d577dd5e2559de29fd31eb06996928b822586ed6296914f`.

The guide distinguishes fixed-code Nice FLO from rolling-code FLOR-S, complete card images from UID-only reads, UART bridge functionality from an SWD probe, and external Wi-Fi hardware from the Flipper itself.

## Verification boundaries

Synthetic script tests and source / SDK compilation are software checks. No Flipper, card, remote control, receiver or gate was connected or tested in this task. Physical-device results remain to be verified on the reader's own or authorized bench.

## Recovery

The change is isolated to this directory and one entry in each bilingual homepage. Revert the commit adding this directory to undo the publication. Rebuild deterministically with `python3 build.py` after editing the guide.
