import cv2


def noise_remove_cv2(image_name, k):
    """
    Noise reduction using an 8-neighborhood approach

    :param image_name: the image to process.
    :param k: the threshold of the number of pixels in the neighborhood.
    """
    def calculate_noise_count(img_obj, w, h):
        """
        Calculate the number of pixels in the neighborhood
        
        :param img_obj: the image to process.
        :param w: the width of the pixel.
        :param h: the height of the pixel.
        """
        
        count = 0
        width, height = img_obj.shape
        for _w_ in [w - 1, w, w + 1]:
            for _h_ in [h - 1, h, h + 1]:
                if _w_ > width - 1:
                    continue
                if _h_ > height - 1:
                    continue
                if _w_ == w and _h_ == h:
                    continue
                if img_obj[_w_, _h_] < 230:  # Assuming binary image with 255 as white
                    count += 1
        return count

    img = cv2.imread(r"auth_data\original/2023-12-13_11-24-08__0998.png", 1)
    # Convert to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    w, h = gray_img.shape
    for _w in range(w):
        for _h in range(h):
            if _w == 0 or _h == 0:
                gray_img[_w, _h] = 255
                continue
            # Count the number of pixels less than 255 in the neighborhood
            pixel = gray_img[_w, _h]
            if pixel == 255:
                continue

            if calculate_noise_count(gray_img, _w, _h) < k:
                gray_img[_w, _h] = 255

    return gray_img


import matplotlib.pyplot as plt


# Display the image using Matplotlib
if __name__ == '__main__':
    image_path = "path_to_your_image.jpg"
    processed_image = noise_remove_cv2(image_path, 4)
    plt.imshow(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB))
    plt.title('Processed Image')
    plt.show()
