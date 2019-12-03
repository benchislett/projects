import torch.nn as nn
import torch.nn.functional as F


class CAE(nn.Module):
    def __init__(self, code_bits=1024, width=32, height=32):
        super(CAE, self).__init__()

        # Encoder
        self.conv1 = nn.Conv2d(3, 24, 3, stride=1)
        self.conv2 = nn.Conv2d(24, 32, 3, stride=1)
        self.conv3 = nn.Conv2d(32, 32, 3, stride=1)
        self.conv4 = nn.Conv2d(32, 32, 3, stride=1)
        self.conv5 = nn.Conv2d(32, 48, 3, stride=1)
        self.conv6 = nn.Conv2d(48, 3, 3, stride=1)
        self.linear_in = nn.Linear(width * height * 3, code_bits)

        # Decoder
        self.linear_out = nn.Linear(code_bits, width * height * 3)
        self.deconv1 = nn.ConvTranspose2d(3, 48, 3, stride=1)
        self.deconv2 = nn.ConvTranspose2d(48, 32, 3, stride=1)
        self.deconv3 = nn.ConvTranspose2d(32, 32, 3, stride=1)
        self.deconv4 = nn.ConvTranspose2d(32, 32, 3, stride=1)
        self.deconv5 = nn.ConvTranspose2d(32, 24, 3, stride=1)
        self.deconv6 = nn.ConvTranspose2d(24, 3, 3, stride=1)

    def encode(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))
        x = F.relu(self.conv5(x))
        x = F.relu(self.conv6(x))
        x = F.sigmoid(self.linear_in(x))
        return x

    def decode(self, x):
        x = F.relu(self.linear_out(x))
        x = F.relu(self.deconv1(x))
        x = F.relu(self.deconv2(x))
        x = F.relu(self.deconv3(x))
        x = F.relu(self.deconv4(x))
        x = F.relu(self.deconv5(x))
        x = self.deconv6(x)
        return x.clamp(min=0, max=255)

    def forward(self, x):
        return self.decode(self.encode(x))
