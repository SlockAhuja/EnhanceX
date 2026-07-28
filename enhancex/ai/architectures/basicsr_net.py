try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False


if HAS_TORCH:
    class BasicSRBlock(nn.Module):
        def __init__(self, num_feat=64):
            super().__init__()
            self.conv1 = nn.Conv2d(num_feat, num_feat, 3, 1, 1)
            self.conv2 = nn.Conv2d(num_feat, num_feat, 3, 1, 1)
            self.relu = nn.ReLU(inplace=True)

        def forward(self, x):
            return x + self.conv2(self.relu(self.conv1(x)))


    class BasicSRNet(nn.Module):
        """BasicSR Residual Architecture for Image & Video Restoration."""
        def __init__(self, num_in_ch=3, num_out_ch=3, num_feat=64, num_blocks=8):
            super().__init__()
            self.conv_in = nn.Conv2d(num_in_ch, num_feat, 3, 1, 1)
            self.body = nn.Sequential(*[BasicSRBlock(num_feat) for _ in range(num_blocks)])
            self.conv_out = nn.Conv2d(num_feat, num_out_ch, 3, 1, 1)

        def forward(self, x):
            feat = F.relu(self.conv_in(x))
            feat = self.body(feat)
            return self.conv_out(feat)
else:
    class BasicSRNet:
        def __init__(self, *args, **kwargs):
            pass
