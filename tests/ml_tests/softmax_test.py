import numpy as np

from src.ml.layers.linear import Linear
from src.ml.layers.module import Module
from src.ml.losses import softmax_loss
from src.ml.optimizers.sgd import SGD


class Example(Module):
    def __init__(self):
        super().__init__()
        self.fc1 = Linear(784, 30)
        self.fc2 = Linear(30, 10)

    def forward(self, x):
        x = self.fc1(x)
        x = self.fc2(x)
        return x

    def backward(self, dout):
        grads = {}
        dx2, dw2, db2 = self.fc2.backward(dout)
        grads["fc2"] = {"w": dw2, "b": db2}
        _, dw1, db1 = self.fc1.backward(dx2)
        grads["fc1"] = {"w": dw1, "b": db1}
        return grads

    def parameters(self):
        """
        This function returns the parameters of the model that need gradients,
        in the order that they are returned in backward().
        """
        return super().parameters("fc1", "fc2")


def test_softmax(fashion_mnist):
    X_train, y_train, _, _ = fashion_mnist

    model = Example()
    save1 = np.array(model.fc1.w)
    save2 = np.array(model.fc2.w)
    optimizer = SGD(model)  # hook into all parameters
    out = model(X_train)
    loss, dx = softmax_loss(out, y_train)
    grads = model.backward(dx)
    optimizer.step(model, grads)
    print(loss)
    assert not (model.fc1.w == save1).all()
    assert not (model.fc2.w == save2).all()
