import numpy as np


def process_image(image_path, detector):
    """Accept only images containing exactly one detectable face."""
    try:
        faces = detector.detect_faces(image_path)
    except Exception as exc:
        return {'status': 'MANUAL_REVIEW', 'reason': f'IMAGE_ERROR: {exc}'}

    if len(faces) == 0:
        return {'status': 'MANUAL_REVIEW', 'reason': 'NO_FACE_DETECTED'}

    if len(faces) != 1:
        return {
            'status': 'MANUAL_REVIEW',
            'reason': f'{len(faces)}_FACES_DETECTED'
        }

    face = faces[0]
    embedding = np.asarray(face.embedding, dtype=np.float32)
    norm = np.linalg.norm(embedding)
    if norm == 0:
        return {'status': 'MANUAL_REVIEW', 'reason': 'INVALID_EMBEDDING'}

    return {
        'status': 'READY',
        'embedding': embedding / norm,
        'detection_score': float(face.det_score)
    }
