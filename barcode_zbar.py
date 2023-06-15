import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np
import psycopg2

# Establish the connection
conn = psycopg2.connect(
    host="localhost",
    database="purches",
    user="postgres",
    password="postgres"
)

def decode(img):
    decodedObjects = pyzbar.decode(img)
    return decodedObjects

def display(img, decodedObjects):
  for decodedObject in decodedObjects:
    points = decodedObject.rect
    # if len(points) > 4 :
    #   hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
    #   hull = list(map(tuple, np.squeeze(hull)))
    # else :
    #   hull = points;
    # n = len(hull)
    # for j in range(0,n):
    #   cv2.line(img, hull[j], hull[ (j+1) % n], (255,0,0), 3)

    cv2.rectangle(frame,(points[0],points[1]),(points[0]+points[2],points[1]+points[3]),(0,255,0),3)
    cv2.putText(img, decodedObject.data.decode(),(100,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
  cv2.imshow("Results", img);
  return None

def fetchReceipt(decodedTexts):
  cursor = conn.cursor()
  query = "SELECT * FROM receipts WHERE receipt_number in ('{}');".format(str(decodedTexts))
  cursor.execute(query)
  rows = cursor.fetchall()
  if(len(rows)==0):
    print("No records found!!")
    return
  for row in rows:
      print(row)
  cursor.close()
  conn.close()
  return None


if __name__ == '__main__':
    vid = cv2.VideoCapture(0)
    while(True):
        ret, frame = vid.read()
        # frame = cv2.imread('barcode.jpg')
        # frame = cv2.imread('qr_code.png')
        # cv2.imshow('frame', frame)
        decodedframe = decode(frame)
        if (decodedframe!=[]):
          for i in decodedframe:
            fetchReceipt(i.data.decode())
          break
        display(frame, decodedframe)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()