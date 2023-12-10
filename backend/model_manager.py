""" This module manages the model and tokenizer. """
import threading
import torch
from transformers import AutoModelForCausalLM, LlamaTokenizer
from loguru import logger

# Global variables to hold the model and tokenizer
MODEL = None
TOKENIZER = None
model_loaded_event = threading.Event()

def load_model():
    """ Load the model. """
    global TOKENIZER, MODEL
    try:
        TOKENIZER = LlamaTokenizer.from_pretrained('lmsys/vicuna-7b-v1.5')
        MODEL = AutoModelForCausalLM.from_pretrained(
            'THUDM/cogvlm-chat-hf',
            torch_dtype=torch.bfloat16,
            low_cpu_mem_usage=True,
            trust_remote_code=True
        ).to('cuda').eval()
        logger.info("Model loaded successfully.")
        model_loaded_event.set()
    except Exception as e:
        logger.error(f"Error loading model: {e}")

def is_model_loaded():
    """ Check if the model is loaded. """
    return model_loaded_event.is_set()

def get_model():
    """ Get the model. """
    if not is_model_loaded():
        raise RuntimeError("Model is not loaded yet.")
    return MODEL

def get_tokenizer():
    """ Get the tokenizer. """
    return TOKENIZER

def start_model_loading():
    """ Start loading the model in a separate thread. """
    global model_loader_thread
    model_loader_thread = threading.Thread(target=load_model, daemon=True)
    model_loader_thread.start()

def await_model_loading():
    """ Wait for the model to be loaded. """
    global model_loader_thread
    model_loader_thread.join()
