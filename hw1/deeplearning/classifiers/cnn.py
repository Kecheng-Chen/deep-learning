import numpy as np

from deeplearning.layers import *
from deeplearning.fast_layers import *
from deeplearning.layer_utils import *


class ThreeLayerConvNet(object):
    """
    A three-layer convolutional network with the following architecture:

    conv - relu - 2x2 max pool - affine - relu - affine - softmax
    (N, C, H, W)->(N, F, H1, W1)->(N, F, H2, W2)->(N, M)->(N, C)
    H1 = 1+(H+2*pad-filter_height)/stride
    W1 = 1+(W+2*pad-filter_width)/stride
    H2 = 1+(H1-pool_height)/stride2
    W2 = 1+(W1-pool_width)/stride2
    D = F*H2*W2

    The network operates on minibatches of data that have shape (N, C, H, W)
    consisting of N images, each with height H and width W and with C input
    channels.
    """

    def __init__(self, input_dim=(3, 32, 32), num_filters=32, filter_size=7,
                 hidden_dim=100, num_classes=10, weight_scale=1e-3, reg=0.0,
                 dtype=np.float32):
        """
        Initialize a new network.

        Inputs:
        - input_dim: Tuple (C, H, W) giving size of input data
        - num_filters: Number of filters to use in the convolutional layer
        - filter_size: Size of filters to use in the convolutional layer
        - hidden_dim: Number of units to use in the fully-connected hidden layer
        - num_classes: Number of scores to produce from the final affine layer.
        - weight_scale: Scalar giving standard deviation for random initialization
          of weights.
        - reg: Scalar giving L2 regularization strength
        - dtype: numpy datatype to use for computation.
        """
        self.params = {}
        self.reg = reg
        self.dtype = dtype

        ############################################################################
        # TODO: Initialize weights and biases for the three-layer convolutional    #
        # network. Weights should be initialized from a Gaussian with standard     #
        # deviation equal to weight_scale; biases should be initialized to zero.   #
        # All weights and biases should be stored in the dictionary self.params.   #
        # Store weights and biases for the convolutional layer using the keys 'W1' #
        # and 'b1'; use keys 'W2' and 'b2' for the weights and biases of the       #
        # hidden affine layer, and keys 'W3' and 'b3' for the weights and biases   #
        # of the output affine layer.                                              #
        ############################################################################
        W1=np.random.normal(0,weight_scale,(num_filters,input_dim[0],filter_size,filter_size))
        b1=np.zeros((1,num_filters))
        pad=(filter_size - 1) // 2
        stride=1
        pool_height=2
        pool_width=2
        stride2=2
        He1 = int(1+(input_dim[1]+2*pad-filter_size)/stride)
        We1 = int(1+(input_dim[2]+2*pad-filter_size)/stride)
        He2 = int(1+(He1-pool_height)/stride2)
        We2 = int(1+(We1-pool_width)/stride2)
        W2=np.random.normal(0,weight_scale,(int(num_filters*He2*We2),hidden_dim))
        b2=np.zeros((1,hidden_dim))
        W3=np.random.normal(0,weight_scale,(hidden_dim,num_classes))
        b3=np.zeros((1,num_classes))
        self.params["W1"] = W1
        self.params["W2"] = W2
        self.params["W3"] = W3
        self.params["b1"] = b1
        self.params["b2"] = b2
        self.params["b3"] = b3
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        for k, v in self.params.items():
            self.params[k] = v.astype(dtype)

    def loss(self, X, y=None):
        """
        Evaluate loss and gradient for the three-layer convolutional network.

        Input / output: Same API as TwoLayerNet in fc_net.py.
        """
        W1, b1 = self.params['W1'], self.params['b1']
        W2, b2 = self.params['W2'], self.params['b2']
        W3, b3 = self.params['W3'], self.params['b3']

        # pass conv_param to the forward pass for the convolutional layer
        filter_size = W1.shape[2]
        conv_param = {'stride': 1, 'pad': (filter_size - 1) // 2}

        # pass pool_param to the forward pass for the max-pooling layer
        pool_param = {'pool_height': 2, 'pool_width': 2, 'stride': 2}

        scores = None
        ############################################################################
        # TODO: Implement the forward pass for the three-layer convolutional net,  #
        # computing the class scores for X and storing them in the scores          #
        # variable.                                                                #
        ############################################################################
        out,cache1 = conv_relu_pool_forward(X, W1, b1, conv_param, pool_param)
        out,cache2 = affine_relu_forward(out, W2, b2)
        out,cache3 = affine_forward(out, W3, b3)
        scores=out
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        if y is None:
            return scores

        loss, grads = 0, {}
        ############################################################################
        # TODO: Implement the backward pass for the three-layer convolutional net, #
        # storing the loss and gradients in the loss and grads variables. Compute  #
        # data loss using softmax, and make sure that grads[k] holds the gradients #
        # for self.params[k]. Don't forget to add L2 regularization!               #
        ############################################################################
        loss,dx=softmax_loss(out, y)
        loss += 0.5*(self.reg*np.sum(self.params["W1"]**2)+self.reg*np.sum(self.params["W2"]**2)++self.reg*np.sum(self.params["W3"]**2))
        dx,dw,db=affine_backward(dx,cache3)
        grads["W3"] = dw+self.reg*self.params["W3"]
        grads["b3"] = db
        dx,dw,db=affine_relu_backward(dx,cache2)
        grads["W2"] = dw+self.reg*self.params["W2"]
        grads["b2"] = db
        dx,dw,db=conv_relu_pool_backward(dx,cache1)
        grads["W1"] = dw+self.reg*self.params["W1"]
        grads["b1"] = db
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        return loss, grads


pass
