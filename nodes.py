import os
import torch
from omegaconf import OmegaConf
from torchvision.transforms import v2
from .normal_to_height import normal_to_height

# Modules from ComfyUI
import folder_paths
from comfy_api.latest import io

# Modules from ComfyUI-Chord
from chord import ChordModel

def apply_padding(model, mode):
    for layer in [layer for _, layer in model.named_modules() if isinstance(layer, torch.nn.Conv2d)]:
        layer.padding_mode = mode

def apply_circular_padding(model):
    if hasattr(model, 'sd'):
        apply_padding(model.sd.vae, 'circular')
        apply_padding(model.sd.unet, 'circular')
    else:
        apply_padding(model, 'circular')

class ChordLoadModel(io.ComfyNode):
    """Node to load Chord Model"""

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ChordLoadModel",
            display_name="Chord - Load Model",
            category="Chord",
            description="A node to load a Chord model.",
            inputs=[
                io.Combo.Input(
                    "ckpt_name",
                    options=[x for x in folder_paths.get_filename_list("checkpoints") if x.endswith("ckpt")]
                ),
            ],
            outputs=[io.Model.Output("model")],
        )
    
    @classmethod
    def execute(cls, ckpt_name) -> io.NodeOutput:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        if type(ckpt_name) is list:
            ckpt_name = ckpt_name[0]
        ckpt_path = folder_paths.get_full_path("checkpoints", ckpt_name)
        config = OmegaConf.load(os.path.join(os.path.dirname(__file__), "chord/config/chord.yaml"))
        model = ChordModel(config)
        ckpt = torch.load(ckpt_path, map_location="cpu", weights_only=False)
        try:
            model.load_state_dict(ckpt["state_dict"])
        except RuntimeError as e:
            raise RuntimeError('Failed to load model, check if the checkpoint file is correct.\n{}'.format(repr(e)))
        model.to(device)
        model.eval()
        return io.NodeOutput(model)

class ChordMaterialEstimation(io.ComfyNode):
    """Chord Material Estimation Node"""

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ChordMaterialEstimation",
            display_name="Chord - Material Estimation",
            category="Chord",
            description="A node to estimate material maps from a texture image using the Chord model.",
            inputs=[
                io.Model.Input(
                    "model",
                    tooltip="The Chord model used to estimate material."
                ),
                io.Image.Input("image",),
            ],
            outputs=[
                io.Image.Output(display_name="basecolor"),
                io.Image.Output(display_name="normal"),
                io.Image.Output(display_name="roughness"),
                io.Image.Output(display_name="metalness"),
            ]
        )
    
    @classmethod
    def execute(cls, model, image) -> io.NodeOutput:
        device = next(model.parameters()).device
        apply_circular_padding(model)
        image = image.permute(0,3,1,2).to(device)
        ori_h, ori_w = image.shape[-2:]
        x = v2.Resize(size=(1024, 1024), antialias=True)(image)
        with torch.no_grad() as no_grad, torch.autocast(device_type=device.type) as amp:
            output = model(x)
        for key in output.keys():
            output[key] = v2.Resize(size=(ori_h, ori_w), antialias=True)(output[key])
            if output[key].ndim == 4:
                output[key] = output[key].permute(0,2,3,1)
        return io.NodeOutput(output['basecolor'], output['normal'], output['roughness'], output['metalness'])
    
class ChordNormalToHeight(io.ComfyNode):
    """Integrate normal map to height map using Poisson solver with overlapping subregions."""

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ChordNormalToHeight",
            display_name="Chord - Normal to Height",
            category="Chord",
            description="A node to convert normal map to height map using Poisson solver with overlapping subregions.",
            inputs=[
                io.Image.Input("normal"),
            ],
            outputs=[
                io.Image.Output(display_name="height"), 
            ],
        )
    
    @classmethod
    def execute(cls, normal) -> io.NodeOutput:
        normal = normal.permute(0,3,1,2)
        height_var_threshold = 5e-4
        ori_h, ori_w = normal.shape[-2:]
        x = v2.Resize(size=(1024, 1024), antialias=True)(normal)
        height = normal_to_height(x)[None, None].squeeze(1)
        if height.var() < height_var_threshold and height.var() > 0:
            height = normal_to_height(x, skip_normalize_normal=True)[None, None].squeeze(1)

        height = v2.Resize(size=(ori_h, ori_w), antialias=True)(height)
        return io.NodeOutput(height)