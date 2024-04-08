import os
import json
import pyautogui
import datetime
from PIL import Image, ImageDraw, ImageFont

def get_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def mkdir_unless_exist(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def find(folder_path, file_name):
    mkdir_unless_exist(folder_path)
    file_list = os.listdir(folder_path)
    if file_name in file_list:
        return True
    else:
        return False
    
def take_screenshot(filename):
    # 화면 캡처
    screenshot = pyautogui.screenshot()
    
    # 현재 날짜 및 시간을 사용하여 파일 이름 생성
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename_with_timestamp = f"{filename}_{timestamp}.png"
    
    # 파일로 저장
    screenshot.save(filename_with_timestamp)
    print(f"화면이 '{filename_with_timestamp}' 파일로 저장되었습니다.")

def get_image(path):
    img = Image.open(path)
    return img

def draw_rectangles(path, detected_objects):
    image = get_image(path)
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 15)
    except IOError:
        font = ImageFont.load_default()

    for obj in detected_objects:
        label, confidence, (x_min, y_min, x_max, y_max) = obj
        label_with_conf = f"{label} {confidence:.2f}"

        # 상자 그리기 전 좌표 확인 (선택적)
        print(f"Drawing box for {label}: {(x_min, y_min, x_max, y_max)}")

        # 사각형 그리기
        draw.rectangle([(x_min, y_min), (x_max, y_max)], outline="red", width=2)

        # 텍스트 그리기 위치 조정
        text_position = (x_min, y_min - 10 if y_min - 10 > 10 else y_min + 10)
        draw.text(text_position, label_with_conf, fill="red", font=font)