import cv2
import time
from hand_tracking import HandTracker
from gesture_recognition import is_click
from virtual_keyboard_ui import draw_keyboard, get_key_from_position,display_typed_text
from text_input import press_key

def main():
    typed_text = ""
    cursor_pos = 0
    click_cooldown = 0.3  
    last_click_time = 0
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = tracker.find_hands(frame)
        x, y, handLms = tracker.get_finger_tip(frame_shape=frame.shape)

        highlight_key = None
        if x is not None and y is not None:
            highlight_key = get_key_from_position(x, y, frame.shape[1], frame.shape[0])
            current_time = time.time()

            if highlight_key is not None and is_click(handLms, frame.shape):
                if current_time - last_click_time > click_cooldown:
                    if highlight_key == 'Backspace':
                        if cursor_pos > 0:
                            # 刪除游標前的文字
                            typed_text = typed_text[:cursor_pos-1] + typed_text[cursor_pos:]
                            cursor_pos -= 1
                    elif highlight_key == '<':
                        if cursor_pos > 0:
                            cursor_pos -= 1
                    elif highlight_key == '>':
                        if cursor_pos < len(typed_text):
                            cursor_pos += 1
                    elif highlight_key == 'Space':
                        # 在游標位置插入空格
                        typed_text = typed_text[:cursor_pos] + ' ' + typed_text[cursor_pos:]
                        cursor_pos += 1
                    else:
                        # 在游標位置插入字母
                        typed_text = typed_text[:cursor_pos] + highlight_key + typed_text[cursor_pos:]
                        cursor_pos += 1
                    
                    last_click_time = current_time  # 更新冷卻

        
        frame = display_typed_text(frame, typed_text,cursor_pos)
        frame = draw_keyboard(frame, highlight_key)
        
        cv2.imshow("Virtual Keyboard", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
