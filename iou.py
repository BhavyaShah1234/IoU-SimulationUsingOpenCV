import numpy as np
import cv2 as cv

cv.namedWindow('CANVAS', cv.WINDOW_FREERATIO)
cv.resizeWindow('CANVAS', 700, 600)


def empty(a):
    pass


cv.createTrackbar('CANVAS WIDTH', 'CANVAS', 600, 1000, empty)
cv.createTrackbar('CANVAS HEIGHT', 'CANVAS', 600, 1000, empty)
cv.createTrackbar('TRUE XMIN', 'CANVAS', 10, 900, empty)
cv.createTrackbar('TRUE YMIN', 'CANVAS', 10, 900, empty)
cv.createTrackbar('TRUE XMAX', 'CANVAS', 10, 900, empty)
cv.createTrackbar('TRUE YMAX', 'CANVAS', 10, 900, empty)
cv.createTrackbar('PRED XMIN', 'CANVAS', 10, 900, empty)
cv.createTrackbar('PRED YMIN', 'CANVAS', 10, 900, empty)
cv.createTrackbar('PRED XMAX', 'CANVAS', 10, 900, empty)
cv.createTrackbar('PRED YMAX', 'CANVAS', 10, 900, empty)

while True:
    canvas_w = cv.getTrackbarPos('CANVAS WIDTH', 'CANVAS')
    canvas_h = cv.getTrackbarPos('CANVAS HEIGHT', 'CANVAS')
    canvas = np.zeros(shape=(canvas_h, canvas_w, 3), dtype='uint8')

    # ALWAYS RECT1_X1 < RECT1_X2 AND RECT1_Y1 < RECT1_Y2
    true_x1 = cv.getTrackbarPos('TRUE XMIN', 'CANVAS')
    true_y1 = cv.getTrackbarPos('TRUE YMIN', 'CANVAS')
    true_x2 = cv.getTrackbarPos('TRUE XMAX', 'CANVAS')
    true_y2 = cv.getTrackbarPos('TRUE YMAX', 'CANVAS')
    # ALWAYS RECT2_X1 < RECT2_X2 AND RECT2_Y1 < RECT2_Y2
    pred_x1 = cv.getTrackbarPos('PRED XMIN', 'CANVAS')
    pred_y1 = cv.getTrackbarPos('PRED YMIN', 'CANVAS')
    pred_x2 = cv.getTrackbarPos('PRED XMAX', 'CANVAS')
    pred_y2 = cv.getTrackbarPos('PRED YMAX', 'CANVAS')
    canvas[true_y1: true_y2, true_x1: true_x2, 0] = 255
    canvas[pred_y1: pred_y2, pred_x1: pred_x2, 2] = 255

    if true_x1 < true_x2 and true_y1 < true_y2 and pred_x1 < pred_x2 and pred_y1 < pred_y2:
        true_w = true_x2 - true_x1
        true_h = true_y2 - true_y1
        pred_w = pred_x2 - pred_x1
        pred_h = pred_y2 - pred_y1
        common_x1 = max(pred_x1, true_x1)
        common_y1 = max(pred_y1, true_y1)
        common_x2 = min(true_x2, pred_x2)
        common_y2 = min(true_y2, pred_y2)
        common_w = common_x2 - common_x1
        common_h = common_y2 - common_y1
        canvas[common_y1: common_y2, common_x1: common_x2, 0] = 0
        canvas[common_y1: common_y2, common_x1: common_x2, 1] = 255
        canvas[common_y1: common_y2, common_x1: common_x2, 2] = 0
        i = max(0, common_w * common_h)
        u = (true_h * true_w) + (pred_h * pred_w) - i
        iou = i / u
    else:
        iou = np.nan
    print(iou)

    cv.imshow('Canvas', canvas)
    cv.waitKey(1)
