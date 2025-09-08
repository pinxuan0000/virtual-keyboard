import cv2

typed_text = ""
keys = [
    ['Q','W','E','R','T','Y','U','I','O','P'],
    ['A','S','D','F','G','H','J','K','L'],
    ['Z','X','C','V','B','N','M','<','>'],  
    ['Space','Backspace']  
]

def draw_keyboard(img, highlight_key=None):
    h, w, _ = img.shape
    key_h = 50
    key_gap = 10
    offset_y = 200  # 鍵盤垂直位置可調整

    for i, row in enumerate(keys):
        # 每一個按鍵寬度可能不同
        key_widths = [150 if k in ['Space','Backspace'] else 50 for k in row]
        row_width = sum(key_widths) + key_gap*(len(row)-1)
        offset_x = (w - row_width) // 2

        x_pos = offset_x
        for j, key in enumerate(row):
            key_w = key_widths[j]
            y = offset_y + i * (key_h + key_gap)
            color = (200,200,200)
            if highlight_key == key:
                color = (0,255,0)
            cv2.rectangle(img, (x_pos,y), (x_pos+key_w, y+key_h), color, -1)
            if key in ['Space','Backspace','<','>']:
                cv2.putText(img, key, (x_pos+5, y+35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2)
            else:
                cv2.putText(img, key, (x_pos+15, y+35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
            x_pos += key_w + key_gap
    return img

def get_key_from_position(x, y, img_width, img_height):
    """依座標找出對應鍵位"""
    key_h = 50
    key_gap = 10
    offset_y = 200
    for i, row in enumerate(keys):
        key_widths = [150 if k in ['Space','Backspace'] else 50 for k in row]
        row_width = sum(key_widths) + key_gap*(len(row)-1)
        offset_x = (img_width - row_width) // 2

        x_pos = offset_x
        for j, key in enumerate(row):
            key_w = key_widths[j]
            key_y = offset_y + i * (key_h + key_gap)
            if x_pos < x < x_pos + key_w and key_y < y < key_y + key_h:
                return key
            x_pos += key_w + key_gap
    return None

def display_typed_text(img, text, cursor_pos):
    h, w, _ = img.shape
    box_x1, box_y1, box_x2, box_y2 = 20, 20, w-20, 150
    cv2.rectangle(img, (box_x1, box_y1), (box_x2, box_y2), (255,255,255), -1)
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 2, 3)[0]
    text_x = box_x1 + (box_x2 - box_x1 - text_size[0]) // 2
    text_y = box_y1 + (box_y2 - box_y1 + text_size[1]) // 2
    cv2.putText(img, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 3)
    cursor_x = text_x
    if len(text) > 0:
        cursor_x += int(text_size[0] * (cursor_pos / len(text)))
    cv2.line(img, (cursor_x, box_y1+20), (cursor_x, box_y2-20), (128,128,128), 2)
    return img
