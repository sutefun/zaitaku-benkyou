import argparse
import yaml

import numpy as np
import torch
from matplotlib.backends.backend_template import FigureCanvas
from torch.autograd import Variable

from models.yolov3 import *
from utils.utils import *
from utils.parse_yolo_weights import parse_yolo_weights
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt


def main(
        image = None ,
        gpu = -1,
        weights_path=  f"{ Path(__file__).parent }/weights/yolov3.weights",
        background = False
):
    """
    Visualize the detection result for the given image and the pre-trained model.
    """
    print( weights_path )
    my_path = Path( __file__ ).parent

    parser = argparse.ArgumentParser()
    parser.add_argument('--gpu', type=int, default= gpu )
    parser.add_argument('--cfg', type=str, default=my_path/'config/yolov3_default.cfg')
    parser.add_argument('--ckpt', type=str,
                        help='path to the checkpoint file')
    parser.add_argument('--weights_path', type=str,
                        default= weights_path, help='path to weights file')
    parser.add_argument('--image', type=str , default= image )
    parser.add_argument('--background', type=bool,
                        default= background , help='background(no-display mode. save "./output.png")')
    parser.add_argument('--detect_thresh', type=float,
                        default= 0.5 , help='confidence threshold')
    args = parser.parse_args()

    with open(args.cfg, 'r') as f:
        cfg = yaml.load(f)

    imgsize = cfg['TEST']['IMGSIZE']
    model = YOLOv3(cfg['MODEL'])

    confthre = cfg['TEST']['CONFTHRE'] 
    nmsthre = cfg['TEST']['NMSTHRE']

    if args.detect_thresh:
        confthre = args.detect_thresh



    img = imread( args.image )
    if img is None :
        print( "load image failed" )
        print( args.image )
        return

    img_raw = img.copy()[:, :, ::-1].transpose((2, 0, 1))
    img, info_img = preprocess(img, imgsize, jitter=0)  # info = (h, w, nh, nw, dx, dy)
    img = np.transpose(img / 255., (2, 0, 1))
    img = torch.from_numpy(img).float().unsqueeze(0)

    if args.gpu >= 0:
        model.cuda(args.gpu)
        img = Variable(img.type(torch.cuda.FloatTensor))
    else:
        img = Variable(img.type(torch.FloatTensor))

    assert args.weights_path or args.ckpt, 'One of --weights_path and --ckpt must be specified'

    if args.weights_path:
        print("loading yolo weights %s" % (args.weights_path))
        parse_yolo_weights(model, args.weights_path)
    elif args.ckpt:
        print("loading checkpoint %s" % (args.ckpt))
        state = torch.load(args.ckpt)
        if 'model_state_dict' in state.keys():
            model.load_state_dict(state['model_state_dict'])
        else:
            model.load_state_dict(state)

    model.eval()


    with torch.no_grad():
        outputs1 = model(img)
        # np.save("output.npy" , outputs.numpy() )
        # torch.save( outputs1 , "outputs1.pt" )
        out1 = torch.load( "outputs1.pt" )
        rere = torch.equal( outputs1 , out1 )
        outputs = postprocess(outputs1, 80, confthre, nmsthre)

        a = "hoho"


    if outputs[0] is None:
        print("No Objects Deteted!!")
        return

    coco_class_names, coco_class_ids, coco_class_colors = get_coco_label_names()

    bboxes = list()
    classes = list()
    colors = list()

    for x1, y1, x2, y2, conf, cls_conf, cls_pred in outputs[0]:

        cls_id = coco_class_ids[int(cls_pred)]
        print(int(x1), int(y1), int(x2), int(y2), float(conf), int(cls_pred))
        print('\t+ Label: %s, Conf: %.5f' %
              (coco_class_names[cls_id], cls_conf.item()))
        box = yolobox2label([y1, x1, y2, x2], info_img)
        bboxes.append(box)
        classes.append(cls_id)
        colors.append(coco_class_colors[int(cls_pred)])

    # args.background = True

    if args.background:
        import matplotlib
        matplotlib.use('Agg')

    from utils.vis_bbox import vis_bbox

    vis_bbox(
        img_raw, bboxes, label=classes, label_names=coco_class_names,
        instance_colors=colors, linewidth=2)


    if args.background:
        output = Path( "./output" )
        output.mkdir( parents=True , exist_ok=True )
        now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        output /= f"output-{now}.png"
        plt.savefig( output )

        return str( output.absolute() )
        # return  plt_to_qpixmap(plt.gca())
    else :
        plt.show()


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def plt_to_qpixmap(ax) :
    figure = ax.figure
    figure.set_tight_layout(True)
    canvas = figure.canvas
    # canvas = FigureCanvas(figure)
    ax.set_axis_off()
    canvas.draw()

    width, height = figure.get_size_inches() * figure.dpi
    buffer_rgba = canvas.buffer_rgba()
    im = QImage( buffer_rgba , width, height, QImage.Format_RGB32 )

    return QPixmap(im)


if __name__ == '__main__':
    main()
