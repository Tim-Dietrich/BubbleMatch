import cv2

from BubbleMatch.Parameters import PROCESSING_DEBUG


# Applies a manga-like filter to an image
# returns the modified image
def manga_filter1(image, debug_windows=PROCESSING_DEBUG):
    # convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # blur
    blur = cv2.GaussianBlur(gray, (0, 0), sigmaX=33, sigmaY=33)

    # raise contrast on the blurred image
    blur = cv2.addWeighted(blur, 2, blur, 0, 0)

    # divide
    divide = cv2.divide(gray, blur, scale=255)

    # otsu threshold
    # thresh = cv2.threshold(divide, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    # alternative: adaptive thresh
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    # apply morphology
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # display it if debug enabled
    if debug_windows:
        cv2.imshow("gray", gray)
        cv2.imshow("divide", divide)
        cv2.imshow("thresh", thresh)
        cv2.imshow("morph", morph)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return thresh


def manga_filter2(image, debug_windows=PROCESSING_DEBUG):
    # sigma_s and sigma_r are the same as in stylization.
    # shade_factor is a simple scaling of the output image intensity.
    # The higher the value, the brighter is the result. Range 0 - 0.1
    dst_gray, dst_color = cv2.pencilSketch(image, sigma_s=60, sigma_r=0.07, shade_factor=0.05)

    if debug_windows:
        cv2.imshow("gray", dst_gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return dst_gray


def manga_filter3(image, debug_windows=PROCESSING_DEBUG):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # inverted grayscale image
    img_invert = cv2.bitwise_not(gray_img)
    # Gaussian blur to smooth details
    img_smoothing = cv2.GaussianBlur(img_invert, (21, 21), sigmaX=0, sigmaY=0)
    # pencil skectched image using divide
    final_img = cv2.divide(gray_img, 255 - img_smoothing, scale=256)

    if debug_windows:
        cv2.imshow("gray", final_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return final_img


def manga_filter4(image, debug_windows=PROCESSING_DEBUG):
    im1 = manga_filter1(image, False)
    im2, _ = cv2.pencilSketch(image, sigma_s=60, sigma_r=0.07, shade_factor=0.05)

    test = cv2.addWeighted(im1, 0.5, im2, 0.5, -0.0)

    if debug_windows:
        cv2.imshow("gray", test)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return test
