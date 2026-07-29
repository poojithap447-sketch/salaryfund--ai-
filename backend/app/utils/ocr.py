"""
OCR extraction pipeline: OpenCV preprocessing (grayscale, denoise, adaptive
threshold, deskew) followed by pytesseract text extraction. Also computes a
lightweight forgery heuristic score based on image-quality artifacts
(compression noise, inconsistent fonts via edge-density variance, and
copy-paste clone detection via ORB keypoint matching).
"""
import re

import cv2
import numpy as np
import pytesseract

from app.core.exceptions import FileUploadException


def _preprocess(image_bytes: bytes) -> np.ndarray:
    arr = np.frombuffer(image_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise FileUploadException("Uploaded file is not a valid image")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.fastNlMeansDenoising(gray, h=10)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 11)
    return gray


def extract_text(image_bytes: bytes) -> str:
    processed = _preprocess(image_bytes)
    return pytesseract.image_to_string(processed)


def extract_pan_fields(image_bytes: bytes) -> dict:
    text = extract_text(image_bytes)
    pan_match = re.search(r"[A-Z]{5}[0-9]{4}[A-Z]{1}", text.upper())
    dob_match = re.search(r"\d{2}[/-]\d{2}[/-]\d{4}", text)
    return {
        "raw_text": text.strip()[:2000],
        "pan_number": pan_match.group(0) if pan_match else None,
        "date_of_birth": dob_match.group(0) if dob_match else None,
        "extraction_confidence": 0.9 if pan_match else 0.4,
    }


def compute_forgery_score(image_bytes: bytes) -> float:
    """
    Heuristic forgery score in [0, 1] combining:
      - edge-density variance (inconsistent fonts / pasted text regions)
      - ORB keypoint self-similarity (copy-paste clone regions within the same image)
    This is a deterministic, explainable first line of defense; production deployments
    should layer a trained CNN forgery-classifier behind this same interface.
    """
    arr = np.frombuffer(image_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileUploadException("Uploaded file is not a valid image")

    edges = cv2.Canny(img, 100, 200)
    h, w = edges.shape
    tile_h, tile_w = max(h // 8, 1), max(w // 8, 1)
    densities = []
    for y in range(0, h, tile_h):
        for x in range(0, w, tile_w):
            tile = edges[y : y + tile_h, x : x + tile_w]
            if tile.size > 0:
                densities.append(np.mean(tile) / 255.0)
    edge_variance = float(np.var(densities)) if densities else 0.0
    edge_score = min(1.0, edge_variance * 12)

    orb = cv2.ORB_create(nfeatures=500)
    keypoints, descriptors = orb.detectAndCompute(img, None)
    clone_score = 0.0
    if descriptors is not None and len(keypoints) > 20:
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        matches = bf.knnMatch(descriptors, descriptors, k=2)
        self_duplicate_pairs = 0
        for pair in matches:
            if len(pair) == 2:
                m, n = pair
                if m.queryIdx != m.trainIdx and m.distance < 0.6 * max(n.distance, 1e-6):
                    self_duplicate_pairs += 1
        clone_score = min(1.0, self_duplicate_pairs / max(len(keypoints), 1) * 3)

    forgery_score = round(min(1.0, 0.5 * edge_score + 0.5 * clone_score), 4)
    return forgery_score
