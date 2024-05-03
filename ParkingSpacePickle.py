import cv2
import pickle

weight, height = 107, 48

try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        # اضافه کردن مکان به لیست
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1+weight and y1 < y < y1+height:
                # حذف مکان انتخاب شده
                posList.pop(i)
    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)

while True:
    img = cv2.imread('Murteza\parking\carParkImg.png')
    
    # نمایش شماره به همراه مکان پارکینگ
    for i, pos in enumerate(posList):
        x, y = pos
        cv2.rectangle(img, pos, (x+weight, y+height), (255, 255, 0), 2)
        # نوشتن شماره درون مستطیل
        cv2.putText(img, str(i+1), (x+10, y+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback('Image', mouseClick)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    