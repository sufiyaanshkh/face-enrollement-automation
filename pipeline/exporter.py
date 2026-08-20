from pathlib import Path
import shutil
import pandas as pd


def safe_folder_name(name: str) -> str:
    return ''.join('_' if c in '<>:"/\\|?*' else c for c in name).strip()


def export_results(ready_records, manual_records, output_folder):
    output = Path(output_folder)
    ready_dir = output / 'enrollment_ready'
    review_dir = output / 'manual_review'
    output.mkdir(parents=True, exist_ok=True)
    ready_dir.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)

    mapping_rows = []
    for item in ready_records:
        person_dir = ready_dir / safe_folder_name(item['canonical_name'])
        person_dir.mkdir(parents=True, exist_ok=True)
        destination = person_dir / item['filename']
        shutil.copy2(item['filepath'], destination)
        mapping_rows.append({
            'filename': item['filename'],
            'relative_source_path': item['relative_path'],
            'cluster_id': item['cluster_id'],
            'canonical_name': item['canonical_name'],
            'name_variants': ' | '.join(item['name_variants']),
            'name_review_required': item['name_review_required'],
            'detection_score': item['detection_score'],
            'status': item['status'],
            'enrollment_path': str(destination)
        })

    for item in manual_records:
        destination = review_dir / item['filename']
        # Avoid overwriting equal filenames from different subfolders.
        if destination.exists():
            destination = review_dir / f"{Path(item['filename']).stem}__{abs(hash(item['filepath']))}{Path(item['filename']).suffix}"
        shutil.copy2(item['filepath'], destination)

    mapping = pd.DataFrame(mapping_rows)
    manual = pd.DataFrame(manual_records)
    summary = pd.DataFrame([
        {
            'total_ready_images': len(ready_records),
            'total_manual_review_images': len(manual_records),
            'unique_clusters': len(set(x['cluster_id'] for x in ready_records)) if ready_records else 0,
            'name_review_clusters': len(set(x['cluster_id'] for x in ready_records if x['name_review_required']))
        }
    ])

    mapping.to_csv(output / 'identity_mapping.csv', index=False)
    mapping[mapping['status'] == 'READY'].to_csv(output / 'enrollment_ready.csv', index=False)
    manual.to_csv(output / 'manual_review.csv', index=False)

    with pd.ExcelWriter(output / 'cluster_summary.xlsx', engine='openpyxl') as writer:
        mapping.to_excel(writer, sheet_name='Enrollment Mapping', index=False)
        manual.to_excel(writer, sheet_name='Manual Review', index=False)
        summary.to_excel(writer, sheet_name='Summary', index=False)

    return output
