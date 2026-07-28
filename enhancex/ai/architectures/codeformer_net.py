try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False


if HAS_TORCH:
    class CodeFormerBlock(nn.Module):
        def __init__(self, dim):
            super().__init__()
            self.norm = nn.LayerNorm(dim)
            self.fc1 = nn.Linear(dim, dim * 4)
            self.fc2 = nn.Linear(dim * 4, dim)
            self.act = nn.GELU()

        def forward(self, x):
            res = x
            x = self.act(self.fc1(self.norm(x)))
            x = self.fc2(x)
            return x + res


    class CodeFormerNet(nn.Module):
        """CodeFormer VQ-Transformer Architecture for Face Restoration."""
        def __init__(self, dim=256, num_layers=4):
            super().__init__()
            self.encoder = nn.Sequential(
                nn.Conv2d(3, dim // 4, 3, 1, 1),
                nn.ReLU(True),
                nn.Conv2d(dim // 4, dim, 3, 2, 1),
                nn.ReLU(True)
            )
            self.blocks = nn.ModuleList([CodeFormerBlock(dim) for _ in range(num_layers)])
            self.decoder = nn.Sequential(
                nn.ConvTranspose2d(dim, dim // 4, 4, 2, 1),
                nn.ReLU(True),
                nn.Conv2d(dim // 4, 3, 3, 1, 1)
            )

        def forward(self, x):
            feat = self.encoder(x)
            b, c, h, w = feat.shape
            flat_feat = feat.flatten(2).permute(0, 2, 1)
            for block in self.blocks:
                flat_feat = block(flat_feat)
            feat = flat_feat.permute(0, 2, 1).view(b, c, h, w)
            return self.decoder(feat)
else:
    class CodeFormerNet:
        def __init__(self, *args, **kwargs):
            pass
