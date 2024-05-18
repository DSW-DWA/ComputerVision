import cv2
import numpy as np
from tqdm import tqdm


def horn_schunck_optical_flow(prev_frame, next_frame, alpha=0.001, num_iter=100):
    prev_frame = cv2.GaussianBlur(prev_frame, (5, 5), 0).astype(np.float32)
    next_frame = cv2.GaussianBlur(next_frame, (5, 5), 0).astype(np.float32)

    u = np.zeros(prev_frame.shape)
    v = np.zeros(prev_frame.shape)

    Ix = cv2.Sobel(prev_frame, cv2.CV_32F, 1, 0, ksize=3)
    Iy = cv2.Sobel(prev_frame, cv2.CV_32F, 0, 1, ksize=3)
    It = next_frame - prev_frame

    kernel = np.array([[1 / 12, 1 / 6, 1 / 12],
                       [1 / 6, 0, 1 / 6],
                       [1 / 12, 1 / 6, 1 / 12]], dtype=np.float32)

    for _ in range(num_iter):
        u_avg = cv2.filter2D(u, -1, kernel)
        v_avg = cv2.filter2D(v, -1, kernel)
        denominator = (alpha ** 2 + Ix ** 2 + Iy ** 2)
        u_new = u_avg - (Ix * (Ix * u_avg + Iy * v_avg + It)) / denominator
        v_new = v_avg - (Iy * (Ix * u_avg + Iy * v_avg + It)) / denominator

        if np.mean(np.abs(u - u_new)) < 0.01 and np.mean(np.abs(v - v_new)) < 0.01:
            break

        u, v = u_new, v_new

    magnitude = np.sqrt(u ** 2 + v ** 2)
    dynamic_threshold = np.percentile(magnitude, 95)
    u[magnitude < dynamic_threshold] = 0
    v[magnitude < dynamic_threshold] = 0

    return u, v


def lucas_kanade_optical_flow(prev_frame, next_frame, window_size=15):
    lk_params = dict(winSize=(window_size, window_size),
                     maxLevel=3,
                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    p0 = cv2.goodFeaturesToTrack(prev_frame, mask=None,
                                 **dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7))

    p1, st, err = cv2.calcOpticalFlowPyrLK(prev_frame, next_frame, p0, None, **lk_params)

    good_new = p1[st == 1]
    good_old = p0[st == 1]

    return good_old, good_new


def draw_optical_flow_hs(frame, u, v, step=16):
    h, w = frame.shape[:2]
    for y in range(0, h, step):
        for x in range(0, w, step):
            if np.sqrt(u[y, x] ** 2 + v[y, x] ** 2) > 1:  # Draw only significant vectors
                end_point = (int(x + u[y, x] * 10), int(y + v[y, x] * 10))
                cv2.arrowedLine(frame, (x, y), end_point, (0, 255, 0), 1, tipLength=0.3)
    return frame


def draw_optical_flow_lk(frame, good_old, good_new):
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel()
        c, d = old.ravel()
        frame = cv2.line(frame, (int(a), int(b)), (int(c), int(d)), (0, 255, 0), 1)
        frame = cv2.circle(frame, (int(a), int(b)), 3, (0, 255, 0), -1)
    return frame


def process_video(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    ret, prev_frame = cap.read()
    prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width * 2, height))

    with tqdm(total=frame_count, desc="Processing video") as pbar:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            u, v = horn_schunck_optical_flow(prev_frame_gray, frame_gray)
            frame_hs = draw_optical_flow_hs(frame.copy(), u, v)

            good_old, good_new = lucas_kanade_optical_flow(prev_frame_gray, frame_gray)
            frame_lk = draw_optical_flow_lk(frame.copy(), good_old, good_new)

            combined = np.hstack((frame_hs, frame_lk))
            out.write(combined)

            prev_frame_gray = frame_gray
            pbar.update(1)

    cap.release()
    out.release()


video_path = '../assets/6979414-sd_640_360_30fps.mp4'
output_path = 'output_6979414-sd_640_360_30fps.mp4'

process_video(video_path, output_path)
