import cv2
import numpy as np


def get_perspective(p1, p2, p3, p4):
    if p1[0] > p2[0]:
        top_right = p1
        top_left = p2
    else:
        top_right = p2
        top_left = p1
    if p3[0] > p4[0]:
        bot_right = p3
        bot_left = p4
    else:
        bot_right = p4
        bot_left = p3

    return top_left, top_right, bot_left, bot_right


def find_card(frame, sleeve=False):
    tar_height = 680
    tar_width = 480
    dst = np.zeros((tar_height, tar_width))
    art_x1 = int(round(tar_width * (67 / 480.0)))
    art_y1 = int(round(tar_height * (85 / 680.0)))
    art_x2 = int(round(tar_width * (427 / 480.0)))
    art_y2 = int(round(tar_height * (367 / 680.0)))
    art_sleeve_x1 = int(round(tar_width * (77 / 480.0)))
    art_sleeve_y1 = int(round(tar_height * (109 / 680.0)))
    art_sleeve_x2 = int(round(tar_width * (413 / 480.0)))
    art_sleeve_y2 = int(round(tar_height * (372 / 680.0)))

    gaussianKernel = 11
    gaussianSubtract = 2

    width, height, _ = frame.shape
    frame_area = width * height
    frame_perimeter = width + width + height + height

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
                                 gaussianKernel,
                                 gaussianSubtract)

    gray = cv2.erode(gray, np.ones((3, 3), np.uint8), iterations=1)
    gray = cv2.dilate(gray, np.ones((3, 3), np.uint8), iterations=1)
    edges = cv2.Canny(gray, 300, 500)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) >= 1:
        for cnt in range(len(contours)):
            area = cv2.contourArea(contours[cnt], False)
            if area / frame_area > 0.005:
                perimiter = cv2.arcLength(contours[cnt], False)
                if perimiter / frame_perimeter > 0.075:
                    if area / perimiter > 20:
                        hull = contours[cnt]
                        poly = cv2.approxPolyDP(hull, 0.05 * cv2.arcLength(hull, True), True)
                        if len(poly) == 4:
                            poly = poly[:, 0][poly[:, 0][:, 1].argsort()]
                            p1 = (poly[0][0], poly[0][1])
                            p2 = (poly[1][0], poly[1][1])
                            p3 = (poly[2][0], poly[2][1])
                            p4 = (poly[3][0], poly[3][1])
                            [top_left, top_right, bot_left, bot_right] = get_perspective(p1, p2, p3, p4)
                            pts1 = np.float32([top_left, top_right, bot_left, bot_right])
                            pts2 = np.float32(
                                [[0, 0], [tar_width, 0], [0, tar_height], [tar_width, tar_height]])
                            M = cv2.getPerspectiveTransform(pts1, pts2)
                            dst = cv2.warpPerspective(frame, M, (tar_width, tar_height))

                            cv2.imshow("Card", dst)

                            artCrop = dst[art_y1:art_y2, art_x1:art_x2] if sleeve is False \
                                else dst[art_sleeve_y1:art_sleeve_y2, art_sleeve_x1:art_sleeve_x2]

                            return artCrop

    return None


def test(sleeve=False):
    tar_height = 680
    tar_width = 480
    dst = np.zeros((tar_height, tar_width))
    art_x1 = int(round(tar_width * (67 / 480.0)))
    art_y1 = int(round(tar_height * (85 / 680.0)))
    art_x2 = int(round(tar_width * (427 / 480.0)))
    art_y2 = int(round(tar_height * (367 / 680.0)))
    art_sleeve_x1 = int(round(tar_width * (77 / 480.0)))
    art_sleeve_y1 = int(round(tar_height * (109 / 680.0)))
    art_sleeve_x2 = int(round(tar_width * (413 / 480.0)))
    art_sleeve_y2 = int(round(tar_height * (372 / 680.0)))

    gaussianKernel = 11
    gaussianSubtract = 2

    try:
        cap = cv2.VideoCapture(0)

        screen_width = cap.get(3)
        screen_height = cap.get(4)

        # cap.set(13, 0)
        # cap.set(14, 0)
        while cap.isOpened():
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)

            width, height, _ = frame.shape
            frame_area = width * height
            frame_perimeter = width + width + height + height

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
                                         gaussianKernel,
                                         gaussianSubtract)

            gray = cv2.erode(gray, np.ones((3, 3), np.uint8), iterations=1)
            gray = cv2.dilate(gray, np.ones((3, 3), np.uint8), iterations=1)
            edges = cv2.Canny(gray, 300, 500)
            contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            count = 0

            if len(contours) >= 1:
                for cnt in range(len(contours)):
                    area = cv2.contourArea(contours[cnt], False)
                    if area / frame_area > 0.005:
                        perimiter = cv2.arcLength(contours[cnt], False)
                        if perimiter / frame_perimeter > 0.075:
                            if area / perimiter > 20:
                                hull = contours[cnt]
                                poly = cv2.approxPolyDP(hull, 0.05 * cv2.arcLength(hull, True), True)
                                if len(poly) == 4:
                                    count += 1
                                    print count
                                    poly = poly[:, 0][poly[:, 0][:, 1].argsort()]
                                    p1 = (poly[0][0], poly[0][1])
                                    p2 = (poly[1][0], poly[1][1])
                                    p3 = (poly[2][0], poly[2][1])
                                    p4 = (poly[3][0], poly[3][1])
                                    [top_left, top_right, bot_left, bot_right] = get_perspective(p1, p2, p3, p4)
                                    pts1 = np.float32([top_left, top_right, bot_left, bot_right])
                                    pts2 = np.float32(
                                        [[0, 0], [tar_width, 0], [0, tar_height], [tar_width, tar_height]])
                                    M = cv2.getPerspectiveTransform(pts1, pts2)
                                    dst = cv2.warpPerspective(frame, M, (tar_width, tar_height))

                                    cv2.imshow('dst', dst)

                                    artCrop = dst[art_y1:art_y2, art_x1:art_x2] if sleeve is False \
                                        else dst[art_sleeve_y1:art_sleeve_y2, art_sleeve_x1:art_sleeve_x2]

                                    cv2.imshow('art', artCrop)

            cv2.imshow('edges', edges)
            cv2.imshow('contours', frame)

            key = cv2.waitKey(1)

            if key & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    test()



