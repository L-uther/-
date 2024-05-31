from PIL import Image
import numpy as np
import cv2

def count_colors(image_path):
    # 打开图片文件
    img = Image.open(image_path)
    # 将图片转换为numpy数组
    img_array = np.array(img)
    # 获取图片的宽度和高度
    width, height = img.size
    # 初始化一个字典，用于存储每种颜色的计数
    color_count = {}
    # 遍历数组，统计每种颜色的出现次数
    for i in range(height):
        for j in range(width):
            color = tuple(img_array[i, j])
            if color in color_count:
                color_count[color] += 1
            else:
                color_count[color] = 1
    return color_count

def calculate_area(color_count, total_pixels):
    # 计算每种颜色的面积
    color_area = {}
    for color, count in color_count.items():
        area = (count / total_pixels) * 100
        color_area[color] = area
    return color_area

def grayscale_area(image_path):
    # 转化为灰度图像
    gray_image = Image.open(image_path).convert('L')
    gray_image_array = np.array(gray_image)
    gray_image_width, gray_image_height = gray_image.size
    gray_color_count = {}
    for i in range(gray_image_height):
        for j in range(gray_image_width):
            color = gray_image_array[i, j]
            if color in gray_color_count:
                gray_color_count[color] += 1
            else:
                gray_color_count[color] = 1
    gray_total_pixels = sum(gray_color_count.values())
    gray_color_area = calculate_area(gray_color_count, gray_total_pixels)
    return gray_color_area

def convert_grayscale(image_path, threshold):
    image = Image.open(image_path).convert('L')
    width, height = image.size
    for x in range(width):
        for y in range(height):
            gray = image.getpixel((x, y))
            if gray == threshold:
                image.putpixel((x, y), threshold)
            elif gray == 255:
                image.putpixel((x, y), 255)
            else:
                image.putpixel((x, y), 255)
    return image

def calculate_non_white_area(image_path):
    image = Image.open(image_path).convert('L')
    width, height = image.size
    non_white_area = 0
    for x in range(width):
        for y in range(height):
            gray = image.getpixel((x, y))
            if gray != 255:
                non_white_area += 1
    return non_white_area

if __name__ == "__main__":
    image_path = "1.png"
    color_count = count_colors(image_path)
    total_pixels = sum(color_count.values())
    color_area = calculate_area(color_count, total_pixels)
    print("每种颜色的面积：", color_area)
    print("灰度图像中每种颜色的面积：", grayscale_area(image_path))

    picture_no=str(3)
    input_image = picture_no+'.png'
    output_image = picture_no+'output.png'
    converted_image = convert_grayscale(input_image,60)  #目标颜色阈值
    converted_image.save(output_image)

    #计算非白色面积
    non_white_area=calculate_non_white_area(input_image)
    print(non_white_area)

    img = cv2.imread(output_image)
    cv2.imshow("origin", img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)
    cv2.imshow("binary", binary)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0, 0, 255), 3)
    cv2.imshow("result", img)
    cv2.waitKey(0)

    max_area=0
    objective_area=0
    for i in range(len(contours)):
        cnt=contours[i]
        area = cv2.contourArea(cnt)
        if max_area<=area:
            max_area=area

    for j in range(len(contours)):
        cnt=contours[j]
        area = cv2.contourArea(cnt)
        if (area>objective_area) and (area!=max_area):
            objective_area=area

    print(max_area,objective_area)
    print(picture_no+"图的目标占比是"+str(objective_area/non_white_area)+".png")

    objective_img_path=str(picture_no+"图的目标占比是"+str(objective_area/non_white_area))
    objective_img_path=objective_img_path.replace(".", ",")
    print(objective_img_path)

