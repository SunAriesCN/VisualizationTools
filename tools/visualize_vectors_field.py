import cv2
import numpy as np

def vectorize_image(angles, amplitude=None):
    """
    Input:
    angles - angle in degree ranged in [0, 360]
    amplitude - the magnitude of the vector field

    Output:
    hsv2bgr - the field with angles and magnitudes
        have been encode in HSV color space, and 
        this function convert this hsv image into 
        a BGR color space to display by opencv
    """
    shape = angles.shape
    if not amplitude is None:
        assert angles.shape == amplitude.shape
        max_value = np.max(amplitude)
        min_value = np.min(amplitude)
        v = (amplitude - min_value) * 255. / (max_value-min_value) 
    else:
        v = 255*np.ones(shape)

    s = 255*np.ones(shape)
    h = angles * 0.5

    hsv = np.stack([h,s,v], axis=2)
    hsv2bgr = cv2.cvtColor(hsv.astype('uint8'), cv2.COLOR_HSV2BGR)
    return hsv2bgr

import sys

if __name__ == '__main__':
    image = cv2.imread(sys.argv[1], 0)
    image = cv2.resize(image, None, fx=0.3, fy=0.3)
    cv2.imshow('image',image)

    gx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

    g = abs(gx) + abs(gy)
    cv2.imshow('g',g.astype('uint8'))
    theta = np.rad2deg(np.arctan2(gy, gx)) + 180

    hsv2bgr = vectorize_image(theta, g)
    cv2.imshow('hsv2bgr', hsv2bgr)

    xs = np.array(range(0,image.shape[1])).reshape((1,-1))
    ys = np.array(range(0,image.shape[0])).reshape((-1,1))

    rho = abs(xs*np.cos(np.arctan2(gy,gx)) + ys*np.sin(np.arctan2(gy,gx)))
    print rho.shape
    _, mask = cv2.threshold(g.astype('uint8'), 40, 255, cv2.THRESH_BINARY)
    mask = np.stack([mask, mask, mask], axis=-1)
    rho_theta = vectorize_image(theta, rho)
    rho_theta = cv2.bitwise_and(rho_theta, mask)
    cv2.imshow('rho_theta', rho_theta)
    cv2.waitKey(0)

