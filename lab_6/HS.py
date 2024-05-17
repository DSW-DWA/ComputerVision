import numpy as np
import cv2

def horn_schunck(I1, I2, alpha, num_iterations):
    I1 = cv2.cvtColor(I1, cv2.COLOR_BGR2GRAY)
    I2 = cv2.cvtColor(I2, cv2.COLOR_BGR2GRAY)
    
    Ix = cv2.Sobel(I1, cv2.CV_64F, 1, 0, ksize=5)
    Iy = cv2.Sobel(I1, cv2.CV_64F, 0, 1, ksize=5)
    It = I2 - I1
    
    u = np.zeros(I1.shape)
    v = np.zeros(I1.shape)
    
    kernel = np.array([[1/12, 1/6, 1/12],
                       [1/6,  0,   1/6],
                       [1/12, 1/6, 1/12]])
    
    for _ in range(num_iterations):
        u_avg = cv2.filter2D(u, -1, kernel)
        v_avg = cv2.filter2D(v, -1, kernel)
        
        P = Ix * u_avg + Iy * v_avg + It
        D = alpha**2 + Ix**2 + Iy**2
        
        u = u_avg - Ix * (P / D)
        v = v_avg - Iy * (P / D)
    
    return u, v

def draw_flow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
    fx, fy = flow[y, x].T

    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    for (x1, y1), (x2, y2) in lines:
        cv2.line(vis, (x1, y1), (x2, y2), (0, 255, 0), 1)
        cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
    return vis

def main():
    cap = cv2.VideoCapture('../assets/cars.mp4')
    
    ret, frame1 = cap.read()
    if not ret:
        print("Failed to read video")
        return

    while(cap.isOpened()):
        ret, frame2 = cap.read()
        if not ret:
            break
        
        alpha = 0.5
        num_iterations = 10
        
        u, v = horn_schunck(frame1, frame2, alpha, num_iterations)
        
        flow = np.dstack((u, v))
        flow_img = draw_flow(cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY), flow)
        
        cv2.imshow('Optical Flow', flow_img)
        
        if cv2.waitKey(30) & 0xFF == 27:
            break
        
        frame1 = frame2
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
