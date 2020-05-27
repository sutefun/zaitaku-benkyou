import numpy as np
import cv2
from utils.utils import preprocess

p1 = cv2.imread( "./innsbruck_result.png" )
u = np.transpose( p1 , (2,0,1) )

# p2 , *p2_info = preprocess( p1 , 1000 , 0 , )

# cv2.imshow( "image" , p1 )
# cv2.imshow( "image" , p2 )

# cv2.waitKey()

pass