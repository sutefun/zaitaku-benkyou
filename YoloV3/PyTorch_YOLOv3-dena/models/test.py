from torch import Tensor
import numpy as np
from models.yolov3 import resblock
import torch

from utils.utils import *

# a = torch.rand( (1,64,64,64) )
# x = a + a
# res1 = resblock( 64 )
#
# b = res1.forward( a )

# a = np.zeros( (10 , 5) )
# a1 = [
#     [ 1 , 2 , 3 , 4 , 5  ],
#     [ 11 , 12 ,13 , 14 ,15 ],
#     [ 21 , 22 , 23 , 24 , 25  ],
#     [ 31 , 32 ,33 , 34 ,35 ],
# ]

# nzero = 50
# a0 = np.arange( 1 , 13 )
# a50_0 = np.zeros( nzero )
#
# dxx = [ 1 , 2 , 3 , 4 , 5  ]
# dxx1 = dxx[  : nzero ]
#
# x1 = min( len(a0) , nzero )
# dt = a0[ : nzero ]
# a50_0[ : x1 ] = dt
#
# a1 = np.arange( 1 , 13 ).reshape( 3,-1 )
# a2 = np.arange( 13 ,25 ).reshape( 3,-1 )
#
# c = np.stack( (a1,a2)  )

# ouz = np.load( "output.npy" )
# ouz = torch.from_numpy(ouz)


ouz = torch.load( "outputs1.pt" )
postprocess( ouz , 80 , 0.5 , 0.45 )

pass