#!/usr/bin/env python3
"""Inspect Flipper SubGhz RAW timing files locally. No RF transmission or dependencies."""
import argparse
from collections import Counter
from html import escape
import json
from pathlib import Path
from statistics import median


def inspect(path, gap_us=5000):
    fields, pulses = {}, []
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        if ':' not in line or line.lstrip().startswith('#'):
            continue
        key, value = (s.strip() for s in line.split(':', 1))
        if key == 'RAW_Data':
            pulses.extend(int(x) for x in value.split())
        else:
            fields[key] = value
    if fields.get('Filetype') != 'Flipper SubGhz RAW File' or fields.get('Protocol') != 'RAW':
        raise ValueError('Expected Flipper SubGhz RAW File / Protocol RAW; decoded key files are different')
    if not pulses or any(x == 0 for x in pulses):
        raise ValueError('Need nonzero signed RAW_Data durations')
    if gap_us <= 0:
        raise ValueError('gap-us must be positive')
    def stats(values):
        if not values:
            return None
        m = median(values)
        return dict(count=len(values), min_us=min(values), max_us=max(values),
                    median_us=m, mad_us=median(abs(x-m) for x in values))
    symbols = [abs(x) for x in pulses if abs(x) < gap_us]
    buckets = Counter(round(x/100)*100 for x in symbols)
    report = dict(frequency_hz=fields.get('Frequency'), preset=fields.get('Preset'),
                  pulse_count=len(pulses), total_duration_us=sum(abs(x) for x in pulses),
                  candidate_gaps=sum(x <= -gap_us for x in pulses), gap_threshold_us=gap_us,
                  high=stats([x for x in pulses if 0 < x < gap_us]),
                  low=stats([-x for x in pulses if -gap_us < x < 0]),
                  histogram_100us=dict(sorted(buckets.items())),
                  note='Timing analysis only. Gaps are candidates, not verified frames. No protocol decoding or key recovery.')
    return report, pulses


def svg(pulses, output):
    # Preserve timing ratios. Only the first 256 edges are rendered to keep output readable.
    shown = pulses[:256]
    total = sum(abs(x) for x in shown)
    x = 35.0
    points = []
    for v in shown:
        y = 95 if v > 0 else 175
        points.extend([(x, y), (x+930*abs(v)/total, y)])
        x += 930*abs(v)/total
    path = ' '.join(f'{x:.2f},{y}' for x,y in points)
    title = f'Demodulated pulse timing · first {len(shown)} durations · {total} µs'
    Path(output).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 240"><title>{escape(title)}</title><rect width="1000" height="240" fill="white"/><text x="35" y="40" font-family="sans-serif" font-size="20">{escape(title)}</text><polyline points="{path}" stroke="#c74c0b" stroke-width="2" fill="none"/><text x="35" y="220" font-family="sans-serif" font-size="16">High = positive µs · Low = negative µs · horizontal distance is proportional to duration</text></svg>', encoding='utf-8')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('capture', type=Path)
    ap.add_argument('--gap-us', type=int, default=5000)
    ap.add_argument('--svg', type=Path)
    args = ap.parse_args()
    try:
        report, pulses = inspect(args.capture, args.gap_us)
        if args.svg:
            svg(pulses, args.svg)
        print(json.dumps(report, indent=2))
    except (ValueError, OSError) as exc:
        ap.exit(2, f'Error: {exc}\n')


if __name__ == '__main__':
    main()
