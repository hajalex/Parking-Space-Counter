import cv2 as cv
import numpy as np
import pickle

# ابعاد مکان پارکینگ
width, height = 107, 48

# باز کردن ویدیو
cap = cv.VideoCapture('Murteza\parking\carPark.mp4')

# باز کردن فایل pickle برای خواندن مکان‌های پارکینگ
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

# تابع بررسی وضعیت هر مکان پارکینگ


def checkParkingSpace(imgPro):
    for i, pos in enumerate(posList):
        x, y = pos
        # برش تصویر مکان پارکینگ
        imgCrop = imgPro[y:y+height, x:x+width]
        # شمارش پیکسل‌های غیرصفر
        count = cv.countNonZero(imgCrop)
        # اگر تعداد پیکسل‌های غیرصفر کمتر از یک مقداری (مثلا 888) باشد، به عنوان خالی شناخته می‌شود
        if count < 888:
            cv.putText(img, 'Empty', (x, y+height-10), fontScale=0.5,
                       thickness=1, fontFace=cv.FONT_HERSHEY_DUPLEX, color=(0, 0, 255))
            cv.putText(img, str(i + 1), (x + width // 2 - 10, y + height //
                       2 + 10), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


# حلقه اصلی برای پخش ویدیو و بررسی مکان‌های پارکینگ
while True:
    # اگر به انتهای ویدیو رسیده، به ابتدای آن برو
    if cap.get(cv.CAP_PROP_POS_FRAMES) == cap.get(cv.CAP_PROP_FRAME_COUNT):
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)

    # خواندن فریم بعدی از ویدیو
    ret, img = cap.read()

    # تبدیل تصویر به حالت خاکستری
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # فیلتر گاوسی برای کاهش نویز
    imgBlur = cv.GaussianBlur(imgGray, (3, 3), 1)

    # تبدیل تصویر به تصویر دودویی با استفاده از آستانه‌ی تطبیقی
    imgThreshold = cv.adaptiveThreshold(
        imgBlur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 16)

    # اعمال فیلتر مدیانی برای کاهش نویزهای کوچک
    imgMedian = cv.medianBlur(imgThreshold, 5)

    # اعمال دیلیشن برای ادغام قطعات و افزایش ضخامت لبه‌ها
    kernel = np.ones((3, 3), np.uint8)
    imgdilate = cv.dilate(imgMedian, kernel, iterations=1)

    # بررسی وضعیت هر مکان پارکینگ
    checkParkingSpace(imgdilate)

    # نمایش تصویر ویدیو
    cv.imshow('parking', img)

    # منتظر ماندن برای خروجی از کاربر
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
