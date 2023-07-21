import cv2, datetime
import numpy as np

def create_mask(frame, vertices, rgb):
    mask = np.zeros_like(frame)
    cv2.fillPoly(mask, [vertices],rgb)
    return mask

def set_resolution_16_9(capture, width=1920, height=1080):

    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

def detect_min_circle_in_frame(frame, vertices,x_center,y_center):
    # Ограничение области видимости в кадре
    x, y, w, h = cv2.boundingRect(vertices)
    frame_roi = frame[y:y+h, x:x+w]

    # Преобразование изображения в оттенки серого
    gray = cv2.cvtColor(frame_roi, cv2.COLOR_BGR2GRAY)

    # Выполнение Гауссового размытия для сглаживания шумов
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Поиск кругов с помощью преобразования Хафа
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                               param1=50, param2=30, minRadius=0, maxRadius=0)

    min_circle = None
    min_circle_radius = float('inf')
    
    # Выбор минимального круга из всех обнаруженных
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            if r < min_circle_radius:
                min_circle_radius = r
                min_circle = (x + x_center, y + y_center, r)

    if min_circle is not None:
        x, y, r = min_circle
        cv2.circle(frame, (x, y), r, (255, 255, 255), 4)

    return frame

def main():
    capture = cv2.VideoCapture(0)  # Используем видеозахват с камеры (можно использовать 1, 2 и т.д. для других устройств)

    # Установка разрешения 16:9
    set_resolution_16_9(capture)

    # Определение размеров кадра
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Определение вершин полигона для области видимости в центре
    rect_width = width // 2
    rect_height = height // 2
    x_center = (width - rect_width) // 2
    y_center = (height - rect_height) // 2
    bottom_left = (x_center, y_center + rect_height)
    bottom_right = (x_center + rect_width, y_center + rect_height)
    top_left = (x_center, y_center)
    top_right = (x_center + rect_width, y_center)
    vertices = np.array([[bottom_left, bottom_right, top_right, top_left]], dtype=np.int32)



    # r, g, b = 255,255,255

    rgb = [(255,0,0),
           (0,255,0),
           (0,0,255)]
    while True:
        time = int((datetime.datetime.now() - datetime.datetime(1, 1, 1, 0, 0)).total_seconds())
        ret, frame = capture.read()

        if not ret:
            print("Ошибка чтения кадра")
            break

        # Создание маски для ограничения области видимости
        mask = create_mask(frame, vertices,rgb[time%3])


        # Применение маски кадру
        frame_with_mask = cv2.bitwise_and(frame, mask)

        # r = (r+10)%256
        # g = (g+10)%256
        # b = (b+10)%256
        # frame_with_mask[:, :, 0] = b
        # frame_with_mask[:, :, 1] = g
        # frame_with_mask[:, :, 2] = r

        # Поиск и отображение минимального круга в области видимости
        frame_with_min_circle = detect_min_circle_in_frame(frame_with_mask, vertices,x_center,y_center)

        cv2.imshow("Обнаружение минимального круга", frame_with_min_circle)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            ret = False
            break


    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
