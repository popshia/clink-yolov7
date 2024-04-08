import cv2

img = cv2.imread("/home/v7/data/noah/casino/data/27d81b09-6.jpg")
print(type(img), img.shape)

cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
