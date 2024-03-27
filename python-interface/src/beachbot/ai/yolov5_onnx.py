from .debrisdetector import DerbrisDetector
import onnxruntime
import numpy as np


class Yolo5Onnx(DerbrisDetector):
    def __init__(self, model_file) -> None:
        super().__init__(model_file)
        providers=["CPUExecutionProvider"]
        if 'TensorrtExecutionProvider' in onnxruntime.get_available_providers():
            print("TODO: Ignore Tensorrt for now!!")
            providers=["CUDAExecutionProvider"]
        elif 'CUDAExecutionProvider' in onnxruntime.get_available_providers():
            providers=["CUDAExecutionProvider"]
        else:
            print("No Gpu acceleration availabe!")
        print("DL providers are:", providers)
        self.session = onnxruntime.InferenceSession(model_file, providers=providers)
        if self.session is None:
            raise ValueError("Failed to load the model " + model_file)
        input_shapes = self.session.get_inputs()[0].shape
        input_type = self.session.get_inputs()[0].type
        self.img_width = input_shapes[3]
        self.img_height = input_shapes[2]
        if "float16" in input_type:
            self.dtype=np.float16
        elif "float32" in input_type:
            self.dtype=np.float32

    def apply_model(self, inputs):  
        inputs = np.swapaxes(np.swapaxes(inputs, 0, -1), -2, -1)[None, :, :, :] / 255.0
        if inputs.dtype != self.dtype:
            inputs = inputs.astype(self.dtype)
        prediction = self.session.run(None, {"images": inputs})
        return self.wrap_detection(prediction[0][0])