import cv2
import mediapipe as mp
import numpy as np
import base64
from io import BytesIO
from PIL import Image

# Calculate angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# Decode base64 image to OpenCV format
def decode_base64_image(encoded_data):
    decoded_bytes = base64.b64decode(encoded_data)
    image = Image.open(BytesIO(decoded_bytes))
    return np.array(image)

# Initialize MediaPipe modules
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Example base64 encoded image string (replace with actual image data)
base64_image = "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"
# Decode the base64 image
image = decode_base64_image(base64_image)

# Convert PIL image to OpenCV BGR format
image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

# Squat counter variablesx``
counter = 0
stage = None
squat_count = 0  # Variable to store number of squats

# Setup MediaPipe Pose instance
with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
    # Recolor image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_rgb.flags.writeable = False

    # Process the image and get the pose results
    results = pose.process(image_rgb)

    # Recolor back to BGR
    image_rgb.flags.writeable = True
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

    # Extract pose landmarks and calculate angle
    try:
        if results.pose_landmarks is not None:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates of landmarks for knee and hip
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            # Calculate angle
            angle = calculate_angle(hip, knee, ankle)

            # Squat counter logic
            if angle > 160:
                stage = "up"
            elif angle < 90:
                stage = "down"
                counter += 1

            # Since we're processing a single image, the squat count will be based on the current stage
            squat_count = counter

            # Print the stage and number of squats
            print(f"Stage: {stage}")
            print(f"Number of Squats: {squat_count}")

    except Exception as e:
        print(f"Error occurred: {e}")
        pass

    # Render squat counter, stage, and squat count on the image
    cv2.rectangle(image_bgr, (0, 0), (300, 80), (245, 117, 16), -1)

    cv2.putText(image_bgr, 'STAGE', (15, 17), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(image_bgr, stage if stage else 'N/A', (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.putText(image_bgr, 'SQUATS', (200, 17), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(image_bgr, str(squat_count), (215, 73), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

    # Draw the landmarks and connections
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image_bgr, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

    # Display the image with squat detection
    cv2.imshow('Squat Detection', image_bgr)

    # Wait for 3 seconds (3000 milliseconds) and close the window
    cv2.waitKey(9000)
    cv2.destroyAllWindows()