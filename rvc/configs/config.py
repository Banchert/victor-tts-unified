import torch
import json
import os

version_config_paths = [
    os.path.join("48000.json"),
    os.path.join("40000.json"),
    os.path.join("32000.json"),
]


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class Config:
    def __init__(self):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.gpu_name = (
            torch.cuda.get_device_name(int(self.device.split(":")[-1]))
            if self.device.startswith("cuda")
            else None
        )
        self.json_config = self.load_config_json()
        self.gpu_mem = None
        self.x_pad, self.x_query, self.x_center, self.x_max = self.device_config()

    def load_config_json(self):
        configs = {}
        for config_file in version_config_paths:
            config_path = os.path.join("rvc", "configs", config_file)
            with open(config_path, "r") as f:
                configs[config_file] = json.load(f)
        return configs

    def device_config(self):
        if self.device.startswith("cuda"):
            self.set_cuda_config()
        else:
            self.device = "cpu"

        # Enhanced GPU memory configuration with better optimization
        if self.gpu_mem is not None:
            if self.gpu_mem <= 4:
                # Configuration for 4GB GPU memory (Conservative)
                x_pad, x_query, x_center, x_max = (1, 4, 25, 28)
                print(f"GPU Memory: {self.gpu_mem}GB - Using conservative settings for 4GB GPU")
            elif self.gpu_mem <= 6:
                # Configuration for 6GB GPU memory (Balanced)
                x_pad, x_query, x_center, x_max = (1, 5, 30, 32)
                print(f"GPU Memory: {self.gpu_mem}GB - Using balanced settings for 6GB GPU")
            elif self.gpu_mem <= 8:
                # Configuration for 8GB GPU memory (Optimized)
                x_pad, x_query, x_center, x_max = (1, 6, 38, 41)
                print(f"GPU Memory: {self.gpu_mem}GB - Using optimized settings for 8GB GPU")
            elif self.gpu_mem <= 12:
                # Configuration for 12GB GPU memory (High Performance)
                x_pad, x_query, x_center, x_max = (2, 8, 45, 48)
                print(f"GPU Memory: {self.gpu_mem}GB - Using high performance settings for 12GB GPU")
            elif self.gpu_mem <= 16:
                # Configuration for 16GB GPU memory (Very High Performance)
                x_pad, x_query, x_center, x_max = (2, 10, 50, 55)
                print(f"GPU Memory: {self.gpu_mem}GB - Using very high performance settings for 16GB GPU")
            elif self.gpu_mem <= 24:
                # Configuration for 24GB GPU memory (Ultra Performance)
                x_pad, x_query, x_center, x_max = (3, 12, 60, 65)
                print(f"GPU Memory: {self.gpu_mem}GB - Using ultra performance settings for 24GB GPU")
            else:
                # Configuration for >24GB GPU memory (Maximum Performance)
                x_pad, x_query, x_center, x_max = (4, 15, 70, 75)
                print(f"GPU Memory: {self.gpu_mem}GB - Using maximum performance settings for high-end GPU")
        else:
            # Default configuration for unknown GPU memory
            x_pad, x_query, x_center, x_max = (1, 6, 38, 41)
            print("GPU Memory: Unknown - Using default settings")

        return x_pad, x_query, x_center, x_max

    def set_cuda_config(self):
        i_device = int(self.device.split(":")[-1])
        self.gpu_name = torch.cuda.get_device_name(i_device)
        self.gpu_mem = torch.cuda.get_device_properties(i_device).total_memory // (
            1024**3
        )


def max_vram_gpu(gpu):
    if torch.cuda.is_available():
        gpu_properties = torch.cuda.get_device_properties(gpu)
        total_memory_gb = round(gpu_properties.total_memory / 1024 / 1024 / 1024)
        return total_memory_gb
    else:
        return "8"


def get_gpu_info():
    ngpu = torch.cuda.device_count()
    gpu_infos = []
    if torch.cuda.is_available() or ngpu != 0:
        for i in range(ngpu):
            gpu_name = torch.cuda.get_device_name(i)
            mem = int(
                torch.cuda.get_device_properties(i).total_memory / 1024 / 1024 / 1024
                + 0.4
            )
            gpu_infos.append(f"{i}: {gpu_name} ({mem} GB)")
    if len(gpu_infos) > 0:
        gpu_info = "\n".join(gpu_infos)
    else:
        gpu_info = "Unfortunately, there is no compatible GPU available to support your training."
    return gpu_info


def get_number_of_gpus():
    if torch.cuda.is_available():
        num_gpus = torch.cuda.device_count()
        return "-".join(map(str, range(num_gpus)))
    else:
        return "-"
