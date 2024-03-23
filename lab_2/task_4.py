from PIL import Image
import math

def load_image(file_path):
    return Image.open(file_path).convert('L')

def save_image(image, file_path):
    image.save(file_path)

def apply_sobel_operator(image):
    width, height = image.size
    sobel_x = [[-1, 0, 1],
               [-2, 0, 2],
               [-1, 0, 1]]
    sobel_y = [[1, 2, 1],
               [0, 0, 0],
               [-1, -2, -1]]

    new_image = Image.new("L", (width, height))

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            pixel_x = sum(image.getpixel((x + i, y + j)) * sobel_x[i][j] for i in range(-1, 2) for j in range(-1, 2))
            pixel_y = sum(image.getpixel((x + i, y + j)) * sobel_y[i][j] for i in range(-1, 2) for j in range(-1, 2))
            gradient_magnitude = int(math.sqrt(pixel_x**2 + pixel_y**2))
            new_image.putpixel((x, y), gradient_magnitude)

    return new_image

if __name__ == "__main__":
    input_image = load_image("../assets/image_bw.jpg")
    edges_image = apply_sobel_operator(input_image)
    save_image(edges_image, "task_4_result/edges_image_default.jpg")

    input_image = load_image("task_2_result/median_filtered_image.jpg")
    edges_image = apply_sobel_operator(input_image)
    save_image(edges_image, "task_4_result/edges_image_median_filtered.jpg")

    input_image = load_image("task_3_result/sharp_image_rect.jpg")
    edges_image = apply_sobel_operator(input_image)
    save_image(edges_image, "task_4_result/edges_image_rect.jpg")

    input_image = load_image("task_3_result/sharp_image_gauss.jpg")
    edges_image = apply_sobel_operator(input_image)
    save_image(edges_image, "task_4_result/edges_image_gauss.jpg")

    input_image = load_image("task_3_result/sharp_image_gauss.jpg")
    edges_image = apply_sobel_operator(input_image)
    save_image(edges_image, "task_4_result/edges_image_gauss.jpg")

    input_image = load_image("task_3_result/sharp_image_median.jpg")
    edges_image = apply_sobel_operator(input_image)
    save_image(edges_image, "task_4_result/edges_image_median.jpg")