import cv2
import numpy as np

def detect_shape_in_frame(frame):
    # Для обнаружения кругов
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                               param1=50, param2=30, minRadius=0, maxRadius=0)

    # Для обнаружения квадратов
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_area_circle = 0
    max_circle = None
    max_area_square = 0
    max_square = None

    # Поиск наибольшего круга и квадрата
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            area = np.pi * r * r
            if area > max_area_circle:
                max_area_circle = area
                max_circle = (x, y, r)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)

        if len(approx) == 4:
            area = cv2.contourArea(contour)
            if area > max_area_square:
                max_area_square = area
                max_square = contour

    # Рисование обнаруженного круга или квадрата и вывод сообщения
    if max_circle is not None:
        x, y, r = max_circle
        cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
        cv2.putText(frame, "Circle", (x - 30, y + r + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    elif max_square is not None:
        cv2.drawContours(frame, [max_square], 0, (0, 0, 255), 4)
        cv2.putText(frame, "Pup", (max_square[0][0][0] - 50, max_square[0][0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    return frame

def main():
    capture = cv2.VideoCapture(0)  # Используем видеозахват с камеры (можно использовать 1, 2 и т.д. для других устройств)
    count = 0
    while True:
        ret, frame = capture.read()

        if not ret:
            print("Ошибка чтения кадра")
            break

        frame_with_shape = detect_shape_in_frame(frame)

        cv2.imshow("Kadr", frame_with_shape)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            

    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
