# model_manager.py

import torch
from transformers import AutoModelForCausalLM, LlamaTokenizer
import threading
from loguru import logger

# Global variables to hold the model and tokenizer
model = None
tokenizer = None
model_loaded_event = threading.Event()

def load_model():
    global tokenizer, model
    try:
        tokenizer = LlamaTokenizer.from_pretrained('lmsys/vicuna-7b-v1.5')
        model = AutoModelForCausalLM.from_pretrained(
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
    return model_loaded_event.is_set()

def get_model():
    if not is_model_loaded():
        raise RuntimeError("Model is not loaded yet.")
    return model

def get_tokenizer():
    return tokenizer

def start_model_loading():
    global model_loader_thread
    model_loader_thread = threading.Thread(target=load_model, daemon=True)
    model_loader_thread.start()

def await_model_loading():
    global model_loader_thread
    model_loader_thread.join()
