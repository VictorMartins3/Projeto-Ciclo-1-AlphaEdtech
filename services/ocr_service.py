import numpy as np
import easyocr
import cv2


def distance_points(pnt1, pnt2):
    pnt1 = np.array(pnt1)
    pnt2 = np.array(pnt2)
    return np.linalg.norm(pnt2 - pnt1)


def ocr(img_ocr):
    reader = easyocr.Reader(["pt", "en"], gpu=True)
    result = reader.readtext(img_ocr)
    return result


def crop_rotate(img, x1=65, y1=382, x2=201, y2=800):
    cropped_image = img[y1:y2, x1:x2]
    direction = cv2.ROTATE_90_CLOCKWISE
    return cv2.rotate(cropped_image, direction)


def extract_roi(img_ocr, result, key_point):
    min_distance = float("inf")
    closest_bbox = None
    roi_text = None
    for t in result:
        bbox, text, score = t
        height = bbox[3][1] - bbox[0][1]
        if score > 0.3 and height > 26:
            distance = distance_points(key_point, bbox[0])
            if distance < min_distance:
                min_distance = distance
                closest_bbox = bbox
                roi_text = text
    top_left, top_right, bottom_right = (
        closest_bbox[0],
        closest_bbox[1],
        closest_bbox[2],
    )
    w = int(np.linalg.norm(np.array(top_left) - np.array(top_right)))
    h = int(np.linalg.norm(np.array(top_right) - np.array(bottom_right)))
    roi = img_ocr[top_left[1] : top_left[1] + h, top_left[0] : top_left[0] + w]

    return roi, top_left, w, h, roi_text
