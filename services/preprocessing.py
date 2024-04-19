import cv2
import imutils
import numpy as np


def load_image(image_array):
    return cv2.imdecode(image_array, cv2.IMREAD_COLOR)


def gray_scale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def noise_removal(img):
    return cv2.GaussianBlur(img, (5, 5), 0)


def resizer(img, width=500):
    h, w, c = img.shape
    height = int((h / w) * width)
    size = (width, height)
    image = cv2.resize(img, (width, height))
    return image, size


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect


def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array(
        [[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]],
        dtype="float32",
    )
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped


def align_images(img):
    img_re, size = resizer(img)
    detail = cv2.detailEnhance(img_re, sigma_s=20, sigma_r=0.15)
    gray = gray_scale(detail)
    blur = noise_removal(gray)
    edged = cv2.Canny(blur, 75, 200)
    kernel = np.ones((5, 5), np.uint8)
    dilate = cv2.dilate(edged, kernel, iterations=1)
    closing = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)
    contours = cv2.findContours(closing, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
        if len(approx) == 4:
            four_points = np.squeeze(approx)
            break
    # find four points for original image
    multiplier = img.shape[1] / size[0]
    four_points_orig = four_points * multiplier
    four_points_orig = four_points_orig.astype(int)
    warped = four_point_transform(img, four_points_orig)
    warped = cv2.resize(warped, (1100,780)).copy()
    warped = cv2.detailEnhance(warped, sigma_s=20, sigma_r=0.20)
    return warped


def preprocess(img_path):
    img = load_image(img_path)
    aligned = align_images(img)
    return img, aligned
