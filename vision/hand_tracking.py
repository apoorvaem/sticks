import cv2
import mediapipe as mp
import time

hands_module = mp.solutions.hands
draw = mp.solutions.drawing_utils

def count_fingers(hand, side):
    points = hand.landmark
    count = 0

    if side == "Right":
        if points[4].x < points[3].x:
            count += 1
    else:
        if points[4].x > points[3].x:
            count += 1

    tips = [8, 12, 16, 20]
    joints = [6, 10, 14, 18]

    for tip, joint in zip(tips, joints):
        if points[tip].y < points[joint].y:
            count += 1

    return count

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Unable to open camera.")
    exit()

time.sleep(1)

with hands_module.Hands(
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as hands:

    while True:
        success, frame = camera.read()

        if not success:
            print("Unable to read frame.")
            break

        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        result = hands.process(rgb)

        if result.multi_hand_landmarks:

            for i, (hand, side_info) in enumerate(
                zip(
                    result.multi_hand_landmarks,
                    result.multi_handedness
                )
            ):

                side = side_info.classification[0].label

                count = count_fingers(
                    hand,
                    side
                )

                point_style = draw.DrawingSpec(
                    color=(0, 100, 0),
                    thickness=3,
                    circle_radius=4
                )

                line_style = draw.DrawingSpec(
                    color=(255, 255, 255),
                    thickness=2
                )

                draw.draw_landmarks(
                    frame,
                    hand,
                    hands_module.HAND_CONNECTIONS,
                    point_style,
                    line_style
                )

                text = f"{side} hand: {count}"

                size, _ = cv2.getTextSize(
                    text,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    2
                )

                text_width, text_height = size

                x = 20
                y = 50 + i * 50

                cv2.rectangle(
                    frame,
                    (x - 5, y - text_height - 8),
                    (x + text_width + 5, y + 8),
                    (255, 255, 255),
                    -1
                )

                cv2.putText(
                    frame,
                    text,
                    (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 0),
                    2
                )

        cv2.imshow(
            "Sticks Finger Counting",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

camera.release()
cv2.destroyAllWindows()