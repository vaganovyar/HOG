from matplotlib.image import imread  # import libraries for read images

# if you want debug remove "#" below
# import time


class HOG:
    # here make class
    def __init__(self, src):
        # open image
        self.image = imread(src)
        self.cut_image = []
        self.arrows_image = []

    def make_mask(self):
        # doing from rgb to wb
        # 0 is black
        # 1 is white
        new_image = []
        for i in self.image:
            new_image.append([(j[0] + j[1] + j[2]) / 3 for j in i])  # mean of rgb
        self.image = new_image.copy()

    def show(self):
        return self.image  # image should be numpy array

    def make_cut_image(self, k):
        # cut image to square 16 * 16
        n = len(self.image)
        m = len(self.image[0])
        self.k = k
        if n % k != 0:
            n = n // k + 1
        else:
            n //= k
        if m % k != 0:
            m = m // k + 1
        else:
            m //= k
        new_cut_image = [[[[0] * k for i in range(k)] for i in range(m)] for i in range(n)]
        for i in range(len(self.image)):
            for j in range(len(self.image[i])):
                y = i // k  # position of square
                x = j // k
                new_cut_image[y][x][i % k][j % k] = self.image[i][j]
        self.cut_image = new_cut_image

    def show_cut_image(self):
        return self.cut_image  # image should be numpy array

    def make_arrows(self):  # make gradient of HOG
        new_arrow_image = []
        for i in self.cut_image:
            arrow = []
            for j in i:
                num_arrow = [0] * 8  # all arrows
                for ii in range(1, self.k - 1):
                    for jj in range(1, self.k - 1):
                        pixels = [j[ii - 1][jj], j[ii - 1][jj + 1], j[ii][jj + 1], j[ii + 1][jj + 1], j[ii + 1][jj],
                                  j[ii + 1][jj - 1], j[ii][jj - 1], j[ii - 1][jj - 1]]
                        way = pixels.index(min(pixels))  # darkest pixel
                        num_arrow[way] += 1  # + one arrow
                arrow.append(num_arrow.index(max(num_arrow)))  # max of arrows in square
            new_arrow_image.append(arrow)
        self.arrows_image = new_arrow_image.copy()

    def show_arrows(self):  # out of HOG arrow
        normal_arrows = [[] for i in range(len(self.arrows_image))]
        for line in range(len(self.arrows_image)):
            for arrow in self.arrows_image[line]:
                if arrow == 0 or arrow == 5:
                    normal_arrows[line].append("|")
                elif arrow == 1 or arrow == 6:
                    normal_arrows[line].append("/")
                elif arrow == 2 or arrow == 7:
                    normal_arrows[line].append("-")
                elif arrow == 3 or arrow == 8:
                    normal_arrows[line].append(chr(92))
        return normal_arrows


"""debugging"""
"""
t = time.time()
a = HOG("path_to_your_image.png")
a.make_mask()
a.make_cut_image(8)
a.make_arrows()
b = a.show_arrows()
print(time.time() - t)
for i in b:
    for j in i:
        print(j, end=" ")
    print()
"""
