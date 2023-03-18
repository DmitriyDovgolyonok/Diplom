from dataset import to_device, get_device, get_image
from model import get_model
import torch
import config


def predict_single():
    image = get_image(config.PATH)
    device = get_device()
    model = get_model()
    model.eval()
    xb = image.unsqueeze(0)
    xb = to_device(xb, device)
    preds = model(xb)

    pred_probs = torch.nn.functional.softmax(preds, dim = 1)[0].tolist()
    class_probs = [(config.IDX_CLASS_LABELS[i], round(pred_probs[i], 4)) for i in range(len(config.IDX_CLASS_LABELS))]
    class_probs = sorted(class_probs, key = lambda x: x[1], reverse = True)

    return tuple(class_probs)


def decode_target(target, text_labels = True):
    result = []
    if text_labels:
        return config.IDX_CLASS_LABELS[target]
    else:
        return target
