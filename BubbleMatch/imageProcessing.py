import cv2

# Applies a manga-like filter to an image
# returns the modified image
def manga_filter(image, debug_windows=False):
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

    morph = cv2.cvtColor(morph, cv2.COLOR_GRAY2RGB)

    # display it if debug enabled
    if debug_windows:
        cv2.imshow("gray", gray)
        cv2.imshow("divide", divide)
        cv2.imshow("thresh", thresh)
        cv2.imshow("morph", morph)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return morph
