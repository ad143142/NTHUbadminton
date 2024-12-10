import numpy as np
import os
import time

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from tensorflow import keras


class Decaptcha:

    def __init__(self, model_path):
        self.model = keras.models.load_model(model_path, compile=False)

    def imgPathDecaptcha(self, image_paths):
        data = []
        for pth in image_paths:
            data.append(img_to_array(load_img(pth)) / 255.0)
        data = np.stack(data)
        # print(data.shape)
        # start = time.time()
        predictions = self.model(data)
        ans = []
        for j in range(len(data)):
            pred_str = ''
            for i in range(4):
                pred_str += str(np.argmax(predictions[i][j]))
            ans.append(pred_str)
        # print('first three data: '+ans)
        # end = time.time()
        # print('time: ', end - start)
        return ans

    def imgDecaptcha(self, images):
        data = []
        for img in images:
            data.append(img / 255.0)
        data = np.stack(data)
        predictions = self.model(data)
        ans = []
        for j in range(len(data)):
            pred_str = ''
            for i in range(4):
                pred_str += str(np.argmax(predictions[i][j]))
            ans.append(pred_str)

        return ans


if __name__ == '__main__':
    model_path = 'C:\\Users\\bywang\\Desktop\\captcha\\god\\god.h5'
    test_img_path = 'C:\\Users\\bywang\\Desktop\\captcha\\test_raw\\eeclass_img0.png'
    test_img = img_to_array(load_img(test_img_path))
    decaptcha = Decaptcha(model_path)
    print(decaptcha.imgPathDecaptcha([test_img_path]))
    print(decaptcha.imgDecaptcha([test_img]))
