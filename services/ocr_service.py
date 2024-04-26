import numpy as np
import easyocr
import cv2


def distance_points(pnt1, pnt2):
    """
    Calculate the Euclidean distance between two points.

    Args:
        pnt1: First point represented as a numpy array.
        pnt2: Second point represented as a numpy array.

    Returns:
        dist: Euclidean distance between the two points.
    """
    pnt1 = np.array(pnt1)
    pnt2 = np.array(pnt2)
    return np.linalg.norm(pnt2 - pnt1)


def ocr(img_ocr):
    """
    Perform optical character recognition (OCR) on the input image.

    Args:
        img_ocr: Input image to be processed.

    Returns:
        result: OCR result containing detected text and associated bounding boxes.
    """
    reader = easyocr.Reader(["pt", "en"], gpu=True)
    result = reader.readtext(img_ocr)
    return result


def crop_rotate(img, x1=65, y1=382, x2=201, y2=800):
    """
    Crop and rotate a region of interest (ROI) from the input image.

    Args:
        img: Input image from which ROI will be extracted.
        x1, y1, x2, y2: Coordinates of the bounding box for cropping.

    Returns:
        cropped_image: Cropped and rotated ROI from the input image.
    """
    cropped_image = img[y1:y2, x1:x2]
    direction = cv2.ROTATE_90_CLOCKWISE
    return cv2.rotate(cropped_image, direction)


def extract_roi(img_ocr, result, key_point, data_type='digit'):
    """
    Extract a region of interest (ROI) containing relevant text from the OCR result.

    Args:
        img_ocr: Input image used for OCR.
        result: OCR result containing detected text and associated bounding boxes.
        key_point: Key point used as reference for extracting the ROI.
        data_type: Type of data to extract ('digit' or 'text').

    Returns:
        roi: Extracted region of interest (ROI) containing relevant text.
        top_left: Coordinates of the top-left corner of the ROI.
        w: Width of the ROI.
        h: Height of the ROI.
        roi_text: Text detected within the ROI.
    """
    # Initialize variables to store minimum distance, closest bounding box, and ROI text
    min_distance = float("inf")
    closest_bbox = None
    roi_text = None
    # Iterate through each detected text bounding box in the OCR result
    for t in result:
        # Extract bounding box, text, and confidence score
        bbox, text, score = t
        # Calculate the height of the bounding box
        height = bbox[3][1] - bbox[0][1]
        # Check if the data type is 'digit'
        if data_type == 'digit':
            # Check if the score is above a threshold, height is sufficient, and text contains digits
            if score > 0.3 and height > 27 and not text.replace(" ", "").isalpha():
                # Calculate the distance between the key point and the top-left corner of the bounding box
                distance = distance_points(key_point, bbox[0])
                # Update the minimum distance and closest bounding box if a closer one is found
                if distance < min_distance:
                    min_distance = distance
                    closest_bbox = bbox
                    roi_text = text
        else:
            # Check if the score is above a threshold and height is sufficient
            if score > 0.3 and height > 27:
                # Calculate the distance between the key point and the top-left corner of the bounding box
                distance = distance_points(key_point, bbox[0])
                # Update the minimum distance and closest bounding box if a closer one is found
                if distance < min_distance:
                    min_distance = distance
                    closest_bbox = bbox
                    roi_text = text

    # Extract the coordinates of the top-left corner of the closest bounding box
    top_left, top_right, bottom_right = (
        closest_bbox[0],
        closest_bbox[1],
        closest_bbox[2],
    )
    # Calculate the width and height of the ROI
    w = int(np.linalg.norm(np.array(top_left) - np.array(top_right)))
    h = int(np.linalg.norm(np.array(top_right) - np.array(bottom_right)))
    # Extract the region of interest (ROI) from the input image
    roi = img_ocr[top_left[1] : top_left[1] + h, top_left[0] : top_left[0] + w]

    return roi, top_left, w, h, roi_text