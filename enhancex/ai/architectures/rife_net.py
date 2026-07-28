try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False


if HAS_TORCH:
    class ConvBlock(nn.Module):
        def __init__(self, in_planes, out_planes, stride=1):
            super().__init__()
            self.conv = nn.Conv2d(in_planes, out_planes, 3, stride, 1)
            self.relu = nn.PReLU()

        def forward(self, x):
            return self.relu(self.conv(x))

    class IFBlock(nn.Module):
        """Intermediate Flow Block for RIFE Architecture."""
        def __init__(self, in_planes, c=64):
            super().__init__()
            self.conv0 = ConvBlock(in_planes, c, stride=2)
            self.conv1 = ConvBlock(c, c, stride=2)
            self.conv2 = ConvBlock(c, c, stride=2)
            self.conv3 = nn.ConvTranspose2d(c, 4, 4, 2, 1)

        def forward(self, x):
            x0 = self.conv0(x)
            x1 = self.conv1(x0)
            x2 = self.conv2(x1)
            flow = self.conv3(x2)
            return flow

    class IFNet(nn.Module):
        """RIFE (Real-Time Intermediate Flow Estimation) Architecture."""
        def __init__(self):
            super().__init__()
            self.block0 = IFBlock(6, c=64)
            self.block1 = IFBlock(10, c=64)
            self.block2 = IFBlock(10, c=64)

        def forward(self, img0, img1, timestep=0.5):
            x = torch.cat((img0, img1), 1)
            flow0 = self.block0(x)
            flow0 = F.interpolate(flow0, scale_factor=4, mode="bilinear", align_corners=False)
            
            warped_img0 = F.grid_sample(img0, flow0[:, :2].permute(0, 2, 3, 1), align_corners=False)
            warped_img1 = F.grid_sample(img1, flow0[:, 2:].permute(0, 2, 3, 1), align_corners=False)

            x1 = torch.cat((img0, img1, warped_img0, warped_img1), 1)
            flow1 = self.block1(x1)
            flow1 = F.interpolate(flow1, scale_factor=4, mode="bilinear", align_corners=False)

            interp_frame = (1.0 - timestep) * warped_img0 + timestep * warped_img1
            return interp_frame
else:
    class IFNet:
        def __init__(self, *args, **kwargs):
            pass
