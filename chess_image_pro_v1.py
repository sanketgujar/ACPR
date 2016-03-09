import cv2
import numpy as np
from matplotlib import pyplot as plt
import subprocess 
import time
import string





def notation(j):

	if(j == 0):
		j ='a' 
	elif(j == 1):
		j ='b'
	elif(j == 2):
		j ='c'
	elif(j == 3):
		j ='d'
	elif(j == 4):
		j ='e'
	elif(j == 5):
		j ='f'
	elif(j == 6):
		j ='g'
	elif(j == 7):
		j ='h'
	return j


clicked = False 
frame = [0 for a in range(50) ]
a = 1


#arr = [[] for _ in range(8)]

#board = [[0 for i in range(8)]for j in range(8)] 
board = np.empty((8, 8), dtype=object)
board_dup = np.empty((8, 8), dtype=object)
board_diff = np.empty((8, 8), dtype=object)

p = subprocess.Popen('gnuchess --xboard',stdin=subprocess.PIPE,stdout = subprocess.PIPE, shell = True)

my_move = p.stdout.readline()
print my_move

'''
def onmouse(event , x, y, param):
	global clicked
	if event == cv2.cv.CV_EVENT_LBUTTONUP:
		clicked	= True
'''

cameraCapture = cv2.VideoCapture(1)
success , fr = cameraCapture.read()

cv2.namedWindow('my_window')
#cv2.setMouseCallback('my	_window',onmouse)
print 'showing camera feed click the window or press any key'

while(1):
	k = cv2.waitKey(33)
	success , fr = cameraCapture.read()
	rows,cols,ch = fr.shape
	pts1 = np.float32([[150,42],[537,34],[158,425],[541,420]])
	pts2 = np.float32([[0,0],[400,0],[0,400],[400,400]])

	M = cv2.getPerspectiveTransform(pts1,pts2)
	fr = cv2.warpPerspective(fr,M,(400,400))
	#fr = cv2.Canny(fr,100,200)	
	if k ==27:
		break
	elif k == -1:
		continue


	elif k == 32:
		
		ret,diff = cv2.threshold(diff,40,255,cv2.THRESH_BINARY)
		diff = cv2.medianBlur(diff,5)
		#diff = cv2.Canny(diff,100,200)	
		plt.hist(diff.ravel(),256,[0,256])
		plt.show()
		cv2.imshow("my_window",diff)
		i = i + 1


	elif k == 65506:						#RIGHT SHIFT KEY
		cv2.imshow("my_window",fr)

	

	elif k == 65505:							#LEFT SHIFT KEY 
		x = 0 
		y = 0
		i = 0
		j = 0
		board_dup =  np.copy(board)
		a=  a +1

		for x in range(0,400,50):
			for y in range(0,400,50):
				block = fr[y+5:y+45, x+5:x+45]
				block = cv2.GaussianBlur(block,(5,5),0)
				block = cv2.cvtColor(block,cv2.COLOR_BGR2GRAY)
				ret , block_b = cv2.threshold(block,50,255,0)
				ret , block_w = cv2.threshold(block,100,255,cv2.THRESH_BINARY_INV)
				contour_b , hie = cv2.findContours(block_b,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
				contour_w , hie = cv2.findContours(block_w,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
				
				cnt_b = contour_b[-1]
				area_b = cv2.contourArea(cnt_b)
				
				cnt_w = contour_w[-1]
				area_w = cv2.contourArea(cnt_w)
				
				if(int(area_b > 1200) & int(area_w > 1200)):
					board[i][j] = 0
				elif(area_w < 1200 ):
					board[i][j] = 2
				else:
					board[i][j] = 1									
				j = j+1
			i=i+1
			j = 0

		print "Chess board detected is shown below"	
		print board




	elif k == 115:
		
		for i in range(0,8,1):
			for j in range(0,8,1):
				board_diff[i][j] = board[i][j] - board_dup[i][j]
		
		i_ini = 0
		j_ini = 0
		i_fin = 0
		j_fin = 0
		#print "subtracted array is shown below"

		for i in range(0,8,1):
			for j in range(0,8,1):
				if(board_diff[i][j] == -1):
						i_ini = i+1
						j_ini = j
				elif(board_diff[i][j] == 1 ):
						i_fin = i+1
						j_fin = j

		j_ini = notation(j_ini)
		j_fin = notation(j_fin)

		tuple1 =i_ini,j_ini
		tuple2 =i_fin,j_fin
		tuple3 =tuple1,tuple2

		print "the move detected is from"
		'''
		print tuple1
		print "----->>>>"
		print tuple2 
		
		print tuple3
		'''
		t = '{0}{1}{2}{3}'.format(j_ini,i_ini,j_fin,i_fin)
		print t
		
		print >> p.stdin,t

		#time.sleep(100)

		for i in range(0,15,1):
			my_move = p.stdout.readline()
			s = my_move[:10]
			if(s == 'My move is'):
				break
		print my_move 
			#my_move = normal_notification(my_move)
		
		try:
			print p.stdout.next()
		except StopIteration:
			pass
		

	else:
		print k


cv2.destroyWindow("my_window")

		
