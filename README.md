# -这张图片计算的是某一块在整个色块的占比，由于相同颜色的分散在不同区域，首先依据目标色块的颜色进行二值化，提取轮廓后判断目标色块的面积在第几位，这个代码提取的色块在第一位，所以只需要提取出轮廓提取后第二位的面积即可，第一位整个图片的面积
