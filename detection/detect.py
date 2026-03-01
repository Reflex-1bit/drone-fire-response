from ultralytics import YOLO
import cv2
import time

# Load model - use fine-tuned model if available, else base
MODEL_PATH = "models/fire_yolov8.pt"  # replace with your fine-tuned model
CONFIDENCE_THRESHOLD = 0.5
CONSECUTIVE_FRAMES_TO_ALERT = 3

model = YOLO(MODEL_PATH)

def detect_fire(source=0):
    """
    Run fire detection on a video file or webcam.
    source: 0 for webcam, or path to video file
    """
    cap = cv2.VideoCapture(source)
    consecutive_detections = 0
    frame_count = 0
    total_detections = 0
    start_time = time.time()

    print(f"[INFO] Starting fire detection on source: {source}")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        results = model(frame, conf=CONFIDENCE_THRESHOLD, verbose=False)
        detections = results[0].boxes

        fire_detected = len(detections) > 0

        if fire_detected:
            consecutive_detections += 1
            total_detections += 1
            annotated = results[0].plot()

            if consecutive_detections >= CONSECUTIVE_FRAMES_TO_ALERT:
                print(f"[ALERT] Fire confirmed at frame {frame_count} — dispatching drones")
                # Hook into swarm coordinator here
                from simulation.swarm_sim import SwarmCoordinator
                coord = SwarmCoordinator()
                coord.dispatch_nearest(fire_location=(frame.shape[1]//2, frame.shape[0]//2))
        else:
            consecutive_detections = 0
            annotated = frame

        elapsed = time.time() - start_time
        fps = frame_count / elapsed if elapsed > 0 else 0
        cv2.putText(annotated, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(annotated, f"Detections: {total_detections}", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Fire Detection", annotated)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    accuracy = (total_detections / frame_count * 100) if frame_count > 0 else 0
    print(f"[INFO] Detection complete. Frames: {frame_count}, Detections: {total_detections}, Rate: {accuracy:.1f}%")


if __name__ == "__main__":
    import sys
    source = sys.argv[1] if len(sys.argv) > 1 else 0
    detect_fire(source)
