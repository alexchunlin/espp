"""Unsent CAN frames by espp::Twai tx_retry_count, ESP32-P4 + two MCP266 nodes, 2026-11-17 bench logs."""
import csv, sys
sys.path.insert(0, "/Users/alxchunlin/code-stuff/alex-style-guide/matplotlib")
import alex_style as ax
import matplotlib.pyplot as plt
ax.use("dark")
# (setting, frames the driver completed with is_tx_success == false, seconds observed, failed SDO poll passes of node 2, passes)
rows = [("tx_retry_count = 3", 341, 106.6, 290, 9717),
        ("tx_retry_count = 15", 232, 72.3, 181, 5823),
        ("tx_retry_count = -1", 39, 2846.1, 0, 283249)]
labels = [r[0] for r in rows]
per_min = [round(r[1] / r[2] * 60, 1) for r in rows]
fig, p = plt.subplots(figsize=(9, 2.9), constrained_layout=True)
ax.bars(p, labels, per_min, highlight=labels[2], unit=" /min", xlabel="Frames reported unsent, per minute", ylabel="Setting")
ax.title(p, "Unsent frames by tx_retry_count on an ESP32-P4",
         "1 Mbit/s, two MCP266 nodes polled at about 1,800 SDO/s. Red: the only setting that retransmits on this controller")
ax.save(fig, "/tmp/mcp-revamp/espp-assets/twai_unsent_frames.png", dpi=160)
with open("/tmp/mcp-revamp/espp-assets/twai_unsent_frames.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["setting", "unsent_frames", "seconds_observed", "unsent_per_minute", "node2_failed_poll_passes", "node2_poll_passes"])
    for r, m in zip(rows, per_min):
        w.writerow([r[0], r[1], r[2], m, r[3], r[4]])
print(per_min)
