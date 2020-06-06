from torch.autograd import Variable
from torch import nn
import torch
from networks import ResnetConditionHR
from collections import OrderedDict
import onnx
from onnx_tf.backend import prepare


class TorchOnnxConverter:
    def __init__(self, torch_model, model_path, test_inputs, output_name, dataparallel=True):
        if dataparallel:
            torch_model = nn.DataParallel(torch_model)
            torch_model.load_state_dict(copy_dict(torch.load(model_path)))
        else:
            torch_model.load_state_dict(torch.load(model_path))
        torch.onnx.export(torch_model, test_inputs, output_name + ".onnx")
        self.onnx_file = output_name + ".onnx"
    @staticmethod
    def copy_dict(state_dict):
        if list(state_dict.keys())[0].startswith("module"):
            start_idx = 1
        else:
            start_idx = 0
        new_state_dict = OrderedDict()
        for k, v in state_dict.items():
            name = ".".join(k.split(".")[start_idx:])
            new_state_dict[name] = v
        return new_state_dict

    def


if __name__ == "__main__":
    # Load the trained model from file
    model_path = 'sample.pth'
    netM = ResnetConditionHR(input_nc=(3, 3, 1, 4), output_nc=4, n_blocks1=7, n_blocks2=3)

    dummy_input1 = Variable(torch.randn(1, 1, 512, 512))
    dummy_input2 = Variable(
        torch.randn(1, 3, 512, 512))  # one black and white 28 x 28 picture will be the input to the model
    dummy_input3 = Variable(torch.randn(1, 4, 512, 512))
    dummy_input = (dummy_input2, dummy_input2, dummy_input1, dummy_input3)
    toc = TorchOnnxConverter(netM,dummy_input,model_path,"sample")
    print("Conversion Complete, New file: {toc.onnx_file}")