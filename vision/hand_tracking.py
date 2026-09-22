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

def game_value(count):
    if count == 5:
        return 0

    return count

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Unable to open camera.")
    exit()

time.sleep(1)

left_count = None
right_count = None

left_previous = None
right_previous = None

left_stable = 0
right_stable = 0

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

        hand_values = {
            "Left": left_count,
            "Right": right_count
        }

        detected_hands = {
            "Left": False,
            "Right": False
        }

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

                detected_hands[side] = True

                if side == "Left":

                    if count == left_previous:
                        left_stable += 1
                    else:
                        left_previous = count
                        left_stable = 1

                    if left_stable >= 5:
                        left_count = game_value(count)

                else:

                    if count == right_previous:
                        right_stable += 1
                    else:
                        right_previous = count
                        right_stable = 1

                    if right_stable >= 5:
                        right_count = game_value(count)

                hand_values[side] = (
                    left_count
                    if side == "Left"
                    else right_count
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

                text = f"{side} hand: {hand_values[side]}"

                x = 20
                y = 50 + i * 50

                cv2.putText(
                    frame,
                    text,
                    (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2
                )

        if not detected_hands["Left"]:
            left_previous = None
            left_stable = 0
            left_count = None

        if not detected_hands["Right"]:
            right_previous = None
            right_stable = 0
            right_count = None

        game_hands = [
            left_count,
            right_count
        ]

        game_text = f"Game state: {game_hands}"

        cv2.putText(
            frame,
            game_text,
            (20, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (50, 255, 100),
            2
        )

        if left_count is not None and right_count is not None:
            status = "READY"
        else:
            status = "WAITING"

        cv2.putText(
            frame,
            status,
            (20, 190),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (50, 255, 100),
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