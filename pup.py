import cv2
from PIL import ImageGrab



def main():

    capture = cv2.VideoCapture(0)

    new_width = 1920
    new_height = 1080

    while True:

        ret, frame = capture.read()

        if not ret:
            print("error")
            break

        resized_frame = cv2.resize(frame, (new_width, new_height))


        cv2.imshow("Kadr", frame)
        

        if cv2.waitKey(1) % 0xFF == ord('q'):
            break
        elif cv2.waitKey(1) % 0xFF == ord('s'):
            cv2.imwrite(f'frame_.png', resized_frame)
        
    capture.release()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()