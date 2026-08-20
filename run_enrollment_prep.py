import argparse
import shutil
from pathlib import Path

from pipeline.image_scanner import scan_images
from pipeline.face_detector import FaceDetector
from pipeline.face_processor import process_image
from pipeline.face_clusterer import cluster_faces
from pipeline.name_cleaner import clean_filename
from pipeline.canonical_name_selector import select_canonical_name
from pipeline.exporter import export_results


def reset_output(output_dir: Path):
    for child in output_dir.iterdir() if output_dir.exists() else []:
        if child.name == '.gitkeep':
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def main():
    parser = argparse.ArgumentParser(description='Prepare profile images for face enrollment.')
    parser.add_argument('--input', default='input/profile_images', help='Folder containing profile images')
    parser.add_argument('--output', default='output', help='Folder for generated enrollment files')
    parser.add_argument('--eps', type=float, default=0.35, help='DBSCAN cosine-distance threshold')
    parser.add_argument('--clear-output', action='store_true', help='Delete previous generated output before running')
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)
    if args.clear_output:
        reset_output(output_dir)

    images = scan_images(input_dir)
    print(f'Found {len(images)} supported images.')
    if not images:
        print('Nothing to process. Add images to the input folder and run again.')
        return

    detector = FaceDetector()
    ready = []
    manual = []

    for index, image_path in enumerate(images, start=1):
        print(f'[{index}/{len(images)}] {image_path.name}')
        result = process_image(image_path, detector)
        base = {
            'filename': image_path.name,
            'filepath': str(image_path.resolve()),
            'relative_path': str(image_path.relative_to(input_dir)),
            'cleaned_name': clean_filename(image_path.name)
        }
        if result['status'] == 'READY':
            base.update(result)
            ready.append(base)
        else:
            base.update(result)
            manual.append(base)

    if ready:
        labels = cluster_faces([item['embedding'] for item in ready], eps=args.eps)
        for item, label in zip(ready, labels):
            item['cluster_id'] = int(label) + 1

        clusters = {}
        for item in ready:
            clusters.setdefault(item['cluster_id'], []).append(item)

        for cluster_id, items in clusters.items():
            canonical, variants, needs_review = select_canonical_name(items)
            for item in items:
                item['canonical_name'] = canonical
                item['name_variants'] = variants
                item['name_review_required'] = needs_review
                item['status'] = 'READY'
                item.pop('embedding', None)

    export_results(ready, manual, output_dir)
    print('\nComplete.')
    print(f'Ready images: {len(ready)}')
    print(f'Manual review: {len(manual)}')
    print(f'Output: {output_dir.resolve()}')


if __name__ == '__main__':
    main()
