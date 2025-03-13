import cv2

# 카메라 열기
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera open failed!")
    exit()

fps = 20.0  # 초당 프레임 수
size = (640, 480)  # 해상도
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 코덱 설정
out = None

recording = False  # 녹화 상태
mode = 0  # 0: 일반, 1: 반전, 2: 윤곽선
flip_horizontal = False  # 좌우반전 여부

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    if flip_horizontal:
        frame = cv2.flip(frame, 1)  # 좌우 반전
    
    processed_frame = frame.copy()
    if mode == 1:
        processed_frame = ~frame
    elif mode == 2:
        edge = cv2.Canny(frame, 50, 150)
        processed_frame = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
    
    if recording:
        if out is None:
            out = cv2.VideoWriter('output_video.avi', fourcc, fps, size)
        out.write(processed_frame)
        cv2.circle(processed_frame, (20, 20), 10, (0, 0, 255), -1)  # 녹화 중 빨간 점 표시
    
    cv2.imshow("Camera View", processed_frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC 키 -> 종료
        break
    elif key == ord('r'):  # r 키 -> 녹화 시작/중지
        recording = not recording
        if not recording and out:
            out.release()
            out = None
    elif key == 32:  # 스페이스바 -> 모드 변경
        mode = (mode + 1) % 3
    elif key == 9:  # TAB 키 -> 좌우 반전 토글
        flip_horizontal = not flip_horizontal

cap.release()
if out:
    out.release()
cv2.destroyAllWindows()