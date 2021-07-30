# import torch
# from torch import nn
# from torch.nn import functional as F
# from torchinfo import summary

# x = torch.randn(10, 3, 256, 256)
# print(sys.getsizeof(x.storage()))

# torch.save(x, "hello.txt")


# class LinearModel(nn.Module):
#     """Linear Model."""

#     def __init__(self) -> None:
#         super().__init__()
#         self.layers = nn.Sequential(
#             nn.Linear(50, 50), nn.ReLU(),
#             nn.Linear(50, 50), nn.ReLU(), nn.Linear(50, 1)
#         )

#     def forward(self, x: torch.Tensor) -> torch.Tensor:
#         x = self.layers(x)
#         return x


# class SingleInputNet(nn.Module):
#     """Simple CNN model."""

#     def __init__(self) -> None:
#         super().__init__()
#         self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
#         self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
#         self.conv2_drop = nn.Dropout2d(0.3)
#         self.fc1 = nn.Linear(320, 50)
#         self.fc2 = LinearModel()

#     def forward(self, x: torch.Tensor) -> torch.Tensor:
#         x = F.relu(F.max_pool2d(self.conv1(x), 2))
#         x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
#         x = x.view(-1, 320)
#         x = F.relu(self.fc1(x))
#         x = self.fc2(x)
#         return F.log_softmax(x, dim=1)


# def main():
#     model = SingleInputNet()
#     result = summary(model, input_size=(8, 1, 28, 28))
#     for layer in result.summary_list:
#         print([name for name, mod in model.named_modules()])
#         d = str(layer.module.__class__)
#         print(d)
#     # summary(net, input_size=(16, 1, 28, 28), cache_forward_pass=True)


# if __name__ == "__main__":
#     main()
