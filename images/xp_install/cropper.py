import cv2
import numpy as np
import os
import glob

INPUT_FOLDER = "C:\\Users\\Viktors\\Desktop\\os_md1\\input"
OUTPUT_FOLDER = "C:\\Users\\Viktors\\Desktop\\os_md1\\output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Maximum preview size
MAX_PREVIEW_W = 1200
MAX_PREVIEW_H = 800

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]  # top-left
    rect[2] = pts[np.argmax(s)]  # bottom-right
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # top-right
    rect[3] = pts[np.argmax(diff)]  # bottom-left
    return rect

def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxWidth = int(max(widthA, widthB))

    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxHeight = int(max(heightA, heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    return cv2.warpPerspective(image, M, (maxWidth, maxHeight))

def resize_for_preview(img, max_w=MAX_PREVIEW_W, max_h=MAX_PREVIEW_H):
    h, w = img.shape[:2]
    scale = min(max_w / w, max_h / h, 1.0)  # never upscale
    return cv2.resize(img, (int(w*scale), int(h*scale))), scale

# Loop over images
for file in glob.glob(f"{INPUT_FOLDER}/*.*"):
    image = cv2.imread(file)
    if image is None:
        print(f"Skipping {file}")
        continue

    clone = image.copy()
    preview, scale = resize_for_preview(clone)
    pts = []

    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Scale click coordinates back to original image size
            orig_x = int(x / scale)
            orig_y = int(y / scale)
            pts.append((orig_x, orig_y))
            cv2.circle(preview, (x, y), 5, (0, 0, 255), -1)
            cv2.imshow("image", preview)

    cv2.imshow("image", preview)
    cv2.setMouseCallback("image", click_event)

    print(f"Click 4 points on {file} in order: top-left, top-right, bottom-right, bottom-left")
    while True:
        key = cv2.waitKey(1) & 0xFF
        if len(pts) == 4:
            break

    warped = four_point_transform(image, np.array(pts))
    out_path = os.path.join(OUTPUT_FOLDER, os.path.basename(file))
    cv2.imwrite(out_path, warped)
    print(f"Saved: {out_path}")

    pts.clear()
    clone = image.copy()

cv2.destroyAllWindows()