from matplotlib import pyplot as plt #type:ignore
from PIL import Image,ImageOps #type:ignore
import numpy as np
from numpy import ndarray


def eeg_to_img(eeg:ndarray)->ndarray:
    
    plt.cla()
    plt.axis('off')
    plt.plot(list(range(eeg.shape[0]) ),eeg.mean(axis=1))
    plt.gcf().canvas.draw()
    img = Image.frombytes('RGB',plt.gcf().canvas.get_width_height(),plt.gcf().canvas.tostring_rgb())
    img = img.resize((64,64))
    # L mode means black and white 8 bit

    img = img.convert("L")
    img = ImageOps.invert(img)

    

    returned = np.asarray(img).reshape(1,64,64)
 
    return returned
        
     
    
