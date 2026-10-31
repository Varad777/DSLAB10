# HeatShield — DSLAB10

**Farmer-Centric Heatwave Monitoring and Early Warning System**  
Data Structures Laboratory — Lab 10  
K.J. Somaiya School of Engineering, Department of Electronics and Computer Engineering

## Team

- Varad Karanjkar — 16014025033
- Asiya Kazi — 16014025035
- Shridula Khandalkar — 16014025036
- Division / Batch: EXCP — A2

## Overview

HeatShield is a menu-driven Python prototype that stores heatwave alerts for agricultural regions and prioritizes the alert with the highest agricultural risk.

Each alert stores:
- Region
- Temperature
- Temperature risk
- Crop risk
- Water risk
- Severity
- Priority score (1–10)

## Data structure

The main data structure is a **Priority Queue implemented using a custom Max Heap backed by a Python list**. The heap is implemented manually; the program does not use `heapq`.

Operations:
- Insert alert — O(log n)
- View highest-priority alert — O(1)
- Delete maximum — O(log n)
- Search region — O(n)
- Delete a specific region — O(n) search plus O(log n) heap repair
- Display heap contents — O(n)

The heap root always contains a maximum-priority alert. The remaining heap-array entries are not necessarily in fully sorted order.

## Priority calculation

The prototype maps risk categories to points:

| Risk | Points |
|---|---:|
| Low | 1 |
| Moderate | 2 |
| High | 3 |
| Critical | 4 |

`Priority Score = Temperature Risk Points + Crop Risk Points + Water Risk Points - 2`

This produces a score from 1 to 10. Severity bands:
- 1–3: Low
- 4–6: Moderate
- 7–8: High
- 9–10: Critical

Temperature risk thresholds used in this educational prototype:
- Below 30°C: Low
- 30°C to below 35°C: Moderate
- 35°C to below 40°C: High
- 40°C and above: Critical

**Important:** These temperature thresholds are illustrative programming assumptions, not official heatwave definitions or crop-specific agronomic advice. They must be calibrated against local agricultural guidance before real-world use.

## Functionalities

1. Add a heatwave alert.
2. Calculate priority and view the highest-risk region.
3. Search for an alert by region.
4. Delete an alert by region.
5. Display all alerts in heap-array order.
6. Generate a farmer warning for the highest-priority alert.
7. Load illustrative demo data.

## Requirements

- Python 3.9 or later
- No external Python packages required

## Run

```bash
python heatshield.py
```

On Windows, this may also be:

```bash
py heatshield.py
```

Choose option `7` to load illustrative demo data, then try options `2`, `3`, `5`, and `6`.

## Repository

Repository name: `DSLAB10`  
Expected URL: https://github.com/Varad777/DSLAB10

## Scope and limitations

This is a command-line educational prototype using manually entered or illustrative data. It does not currently connect to live weather APIs, sensors, databases, or notification services. Farmer warnings are rule-based demonstrations and should not be treated as operational agricultural advice.
