# Berita Dunia — 20 November 2026

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/iwanr94/news-image/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/iwanr94/news-image/reward.svg)](https://make.fun/bounty/news-image-20261120)

A single 1024x1024 front page summarizing the world news of Friday, 20 November 2026,
built for the make.fun `news-image-20261120` bounty. Newspaper/infographic style:
masthead with the date, the ICJ genocide ruling as the lead story, and the rest of the
day's events in a clean card grid.

## What is in the image

| Slot | Story |
| --- | --- |
| Lead | ICJ: Myanmar bersalah genosida atas Rohingya (putusan 9-6, pertama kali bagi pengadilan itu) |
| Rail | KTT tiga pihak Trump-Xi-Putin pertama di Shenzhen; deklarasi damai, tanpa terobosan |
| Grid | Rudal Houthi menghantam menara PIF di Riyadh |
| Grid | Rusia serang Kyiv (8 tewas, 28 luka); Jembatan Kerch diserang ketiga kalinya |
| Grid | Anthropic +17% di debut Nasdaq (~$97 dari IPO $83); Wall Street turun hari ke-5, Nikkei -4,8% |
| Grid | GTA 6 tembus penjualan $2,3 miliar |
| Grid | Kenya memulangkan pasien Ebola terakhir, 37 hari setelah kasus pertama |
| Grid | IMF: utang publik global mendekati 100% PDB; Senat AS tolak resolusi perang Iran 51-48 |

## Files

- `entry.png` — the artifact, 1024x1024, under 1 MiB
- `draw_news.py` — the Pillow renderer (no numpy); every text block is measured and
  raises instead of overflowing its card
- `main.ts` — copies `entry.png` into `$MAKEFUN_OUTPUT_DIR/entry.png` and verifies size

## Build

```bash
python3 draw_news.py                        # renders entry.png
MAKEFUN_OUTPUT_DIR=out node main.ts         # emits out/entry.png
```

Requires Python 3 with Pillow, and Node 22+ (type stripping for `.ts`).

## License

MIT — see [LICENSE](LICENSE).
