def is_click(hand_landmarks, frame_shape):
    """判斷食指是否做點擊動作"""
    if hand_landmarks is None:
        return False
    h, w, _ = frame_shape
    tip_y = hand_landmarks.landmark[8].y * h
    pip_y = hand_landmarks.landmark[6].y * h
    return tip_y > pip_y + 10
