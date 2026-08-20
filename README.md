# Face Enrollment Automation

Prepare a folder of profile images for face-recognition enrollment.

## What it does

1. Recursively scans supported images.
2. Detects faces using InsightFace.
3. Sends images with zero or multiple faces to `manual_review`.
4. Generates normalized face embeddings for valid single-face images.
5. Clusters likely images of the same person using DBSCAN with cosine distance.
6. Cleans filename noise such as `_01`, `_2`, `profile`, and `final`.
7. Suggests one canonical name per cluster and flags clusters with multiple name variants.
8. Generates CSV, Excel, and organized `enrollment_ready/<person>/` folders.

## Clone

```bash
git clone https://github.com/sufiyaanshkh/face-enrollement-automation.git
cd face-enrollement-automation
```

## Setup

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation for the current session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

## Run

Put images inside:

```text
input/profile_images/
```

Then run:

```powershell
python run_enrollment_prep.py --clear-output
```

The first InsightFace run may download model files required by the selected model pack.

## Output

```text
output/
├── identity_mapping.csv
├── enrollment_ready.csv
├── manual_review.csv
├── cluster_summary.xlsx
├── enrollment_ready/
│   └── Canonical Person Name/
└── manual_review/
```

## Output columns

`identity_mapping.csv` contains the original filename, source-relative path, cluster ID, suggested canonical name, all cleaned name variants, whether a name review is required, detection score, and generated enrollment path.

## Important: review before production enrollment

Face clustering and filename-based canonical naming are suggestions, not an authoritative identity system. Any row where `name_review_required=True` should be reviewed or matched against an official personnel list before enrolling under a final identity.

## Tuning clustering

The default clustering threshold is configurable:

```powershell
python run_enrollment_prep.py --eps 0.35 --clear-output
```

Lower values are stricter; higher values merge more faces. Validate this threshold on a representative IIHS dataset before using the output for production enrollment.

## Privacy

Profile images, generated outputs, embeddings, models, and virtual environments are excluded from Git by `.gitignore`. Do not commit profile photographs or biometric data to a public repository.
