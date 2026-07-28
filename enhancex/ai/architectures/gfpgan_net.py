try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False


if HAS_TORCH:
    class StyleGAN2Block(nn.Module):
        def __init__(self, in_ch, out_ch):
            super().__init__()
            self.conv1 = nn.Conv2d(in_ch, out_ch, 3, 1, 1)
            self.conv2 = nn.Conv2d(out_ch, out_ch, 3, 1, 1)
            self.lrelu = nn.LeakyReLU(0.2, inplace=True)

        def forward(self, x):
            return self.lrelu(self.conv2(self.lrelu(self.conv1(x))))


    class GFPGANv1Clean(nn.Module):
        """GFPGAN Face Restoration Generator Architecture."""
        def __init__(self, in_ch=3, out_ch=3, num_feat=64):
            super().__init__()
            self.conv_in = nn.Conv2d(in_ch, num_feat, 3, 1, 1)
            self.block1 = StyleGAN2Block(num_feat, num_feat * 2)
            self.block2 = StyleGAN2Block(num_feat * 2, num_feat * 4)
            self.block3 = StyleGAN2Block(num_feat * 4, num_feat * 2)
            self.conv_out = nn.Conv2d(num_feat * 2, out_ch, 3, 1, 1)

        def forward(self, x):
            feat = F.leaky_relu(self.conv_in(x), 0.2)
            feat = self.block1(feat)
            feat = self.block2(feat)
            feat = self.block3(feat)
            return torch.tanh(self.conv_out(feat))
else:
    class GFPGANv1Clean:
        def __init__(self, *args, **kwargs):
            pass
