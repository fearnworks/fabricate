# caption.py

from PIL import Image
from loguru import logger
from model_manager import get_model, get_tokenizer
import torch


# Function to generate caption for an image
async def generate_image_caption(image: Image) -> str:
    """ This function generates a caption for an image.

    Args:
        image (Image): The image for which to generate a caption.

    Returns:
        str: The generated caption.
    """
    try:
        model = get_model()
        tokenizer = get_tokenizer()
        query = "Describe this image"
        if image is None:
            return "Error fetching image."

        inputs = model.build_conversation_input_ids(
            tokenizer, query=query, history=[], images=[image]
        )
        inputs = {
            "input_ids": inputs["input_ids"].unsqueeze(0).to("cuda"),
            "token_type_ids": inputs["token_type_ids"].unsqueeze(0).to("cuda"),
            "attention_mask": inputs["attention_mask"].unsqueeze(0).to("cuda"),
            "images": [[inputs["images"][0].to("cuda").to(torch.bfloat16)]],
        }
        gen_kwargs = {"max_length": 2048, "do_sample": False}

        with torch.no_grad():
            outputs = model.generate(**inputs, **gen_kwargs)
            outputs = outputs[:, inputs["input_ids"].shape[1] :]
            return tokenizer.decode(outputs[0])
    except Exception as e:
        logger.error(f"Error generating image caption: {e}")
        return "An error occurred while generating the caption."
