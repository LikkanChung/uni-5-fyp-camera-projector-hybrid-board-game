import cv2

def find_anchor_points(image):
    qr_code_detector = cv2.QRCodeDetector()
    codes = qr_code_detector.detectAndDecodeMulti(image)
    print(codes)

