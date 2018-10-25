from captcha.image import ImageCaptcha,random_color
import matplotlib.pyplot as plt
import numpy as np
import random


import string
characters = string.digits
print(characters)

width, height, n_len, n_class = 123, 40, 4, len(characters)

generator = ImageCaptcha(width=width, height=height, font_sizes=[20,30,40])
random_str = ''.join([random.choice(characters) for j in range(4)])

color = random_color(10, 200, random.randint(220, 255))
img = generator.create_captcha_image(chars=random_str, color=color, background='white')
generator.create_noise_curve(img, color=color)
# img = generator.generate_image(random_str)

img.show()
img.save('code.jpg')