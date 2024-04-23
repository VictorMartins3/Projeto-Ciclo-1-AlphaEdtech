import cv2
import imutils
import numpy as np


def load_image(image_array):
    # Decode image array into OpenCV format
    return cv2.imdecode(image_array, cv2.IMREAD_COLOR)


def gray_scale(img):
    # Convert image to grayscale
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def noise_removal(img):
    # Apply Gaussian blur to remove noise
    return cv2.GaussianBlur(img, (5, 5), 0)


def resizer(img, width=500):
    # Resize image while maintaining aspect ratio
    h, w, c = img.shape
    height = int((h / w) * width)
    size = (width, height)
    image = cv2.resize(img, (width, height))
    return image, size


def order_points(pts):
    """
    Order the points of a quadrilateral in top-left, top-right, bottom-right, bottom-left order.
    Args:
        pts: Array of points representing the corners of the quadrilateral.
    Returns:
        rect: Array of ordered points representing the corners of the quadrilateral.
    """
    # Initialize an array to store the ordered points
    rect = np.zeros((4, 2), dtype="float32")
    # Compute the sum of each point's coordinates
    s = pts.sum(axis=1)
    # Find the point with the smallest sum (top-left corner) and largest sum (bottom-right corner)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    # Compute the difference between each point's coordinates
    diff = np.diff(pts, axis=1)
    # Find the point with the smallest difference (top-right corner) and largest difference (bottom-left corner)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect


def four_point_transform(image, pts):
    """
    Apply perspective transformation to warp image.

    Args:
        image: Input image to be warped.
        pts: Array of points representing the corners of the quadrilateral.

    Returns:
        warped: Warped image after perspective transformation.
    """
    # Order the input points of the quadrilateral
    rect = order_points(pts)
    # Extract the ordered points
    (tl, tr, br, bl) = rect
    # Compute the width of the new image
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    # Compute the height of the new image
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    # Define the destination points for the perspective transformation
    dst = np.array(
        [[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]],
        dtype="float32",
    )
    # Compute the perspective transformation matrix
    M = cv2.getPerspectiveTransform(rect, dst)
    # Apply the perspective transformation to warp the image
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped



def align_images(img):
    """
    Align document in image.

    Args:
        img: Input image containing the document.

    Returns:
        warped: Warped and aligned image containing the document.
    """
    # Resize the image
    img_re, size = resizer(img)
    # Enhance image details
    detail = cv2.detailEnhance(img_re, sigma_s=20, sigma_r=0.15)
    # Convert image to grayscale
    gray = gray_scale(detail)
    # Apply Gaussian blur to remove noise
    blur = noise_removal(gray)
    # Detect edges using Canny edge detection
    edged = cv2.Canny(blur, 75, 200)
    # Define a kernel for morphological operations
    kernel = np.ones((5, 5), np.uint8)
    # Dilate the edges to connect nearby contours
    dilate = cv2.dilate(edged, kernel, iterations=1)
    # Perform closing operation to fill gaps in edges
    closing = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)
    # Find contours in the closed image
    contours = cv2.findContours(closing, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    # Sort contours based on area and select the largest ones
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    # Iterate through the contours to find the quadrilateral representing the document
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
        if len(approx) == 4:
            four_points = np.squeeze(approx)
            break
    # Find the four points corresponding to the corners of the document in the original image
    multiplier = img.shape[1] / size[0]
    four_points_orig = four_points * multiplier
    four_points_orig = four_points_orig.astype(int)
    # Apply perspective transformation to align the document
    warped = four_point_transform(img, four_points_orig)
    # Resize the aligned image
    warped = cv2.resize(warped, (1100, 780)).copy()
    # Enhance details in the aligned image
    warped = cv2.detailEnhance(warped, sigma_s=20, sigma_r=0.20)
    return warped



def preprocess(img_path):
    # Preprocess image
    img = load_image(img_path)
    aligned = align_images(img)
    return aligned
