import torch
import torch.nn as nn
from .module import make
from .module.chord import post_decoder

class ChordModel(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.model = make(config.model.name, config.model)

    def forward(self, x: torch.Tensor):
        x = {"render": x}
        pred = self.model(x)
        return post_decoder(pred)