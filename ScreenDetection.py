from transformers import DetrImageProcessor, DetrForObjectDetection
from torch.cuda import is_available
from torch import tensor
import utils

CUDA_device = "cuda:0" if is_available() else "cpu"
model_path = "cache/models--facebook--detr-resnet-50/snapshots/70120ba84d68ca1211e007c4fb61d0cd5424be54"
model_name = "facebook/detr-resnet-50"

class screen_detection():
    def __init__(self):
        self.processor = DetrImageProcessor.from_pretrained(model_path, revision="no_timm", local_files_only=True) if utils.find(model_path, "preprocessor_config.json") else DetrImageProcessor.from_pretrained(model_name, revision="no_timm", cache_dir="cache")
        self.model = DetrForObjectDetection.from_pretrained(model_path, revision="no_timm", local_files_only=True).to(CUDA_device) if utils.find(model_path, "config.json") else DetrForObjectDetection.from_pretrained(model_name, revision="no_timm", cache_dir="cache").to(CUDA_device)

    def detect(self, path, threshold=0.9):
        img = utils.get_image(path)
        inputs = self.processor(images=img, return_tensors="pt")
        inputs.to("cuda:0")
        outputs = self.model(**inputs)

        target_sizes = tensor([img.size[::-1]])
        results = self.processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=threshold)[0]
        
        res = []
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            item = self.model.config.id2label[label.item()]
            confidence = round(score.item(), 3)
            box = [round(i, 2) for i in box.tolist()]
            res.append((item, confidence, box))

        return res