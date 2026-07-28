"""
Neural Network Architectures Module: Real-ESRGAN (RRDBNet), RIFE (IFNet), GFPGAN, CodeFormer, BasicSR.
"""

from enhancex.ai.architectures.rrdbnet import RRDBNet
from enhancex.ai.architectures.rife_net import IFNet
from enhancex.ai.architectures.gfpgan_net import GFPGANv1Clean
from enhancex.ai.architectures.codeformer_net import CodeFormerNet
from enhancex.ai.architectures.basicsr_net import BasicSRNet

__all__ = [
    "RRDBNet",
    "IFNet",
    "GFPGANv1Clean",
    "CodeFormerNet",
    "BasicSRNet"
]
