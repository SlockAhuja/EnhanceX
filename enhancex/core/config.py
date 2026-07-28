import os
import yaml
from typing import Any, Dict, Optional


class ConfigManager:
    """Configuration Manager for loading, parsing, and retrieving settings."""

    _instance: Optional['ConfigManager'] = None

    def __init__(self, config_path: Optional[str] = None):
        self.config: Dict[str, Any] = self._default_config()
        if config_path and os.path.exists(config_path):
            self.load(config_path)

    @classmethod
    def get_instance(cls, config_path: Optional[str] = None) -> 'ConfigManager':
        if cls._instance is None:
            cls._instance = ConfigManager(config_path)
        elif config_path and os.path.exists(config_path):
            cls._instance.load(config_path)
        return cls._instance

    @staticmethod
    def _default_config() -> Dict[str, Any]:
        return {
            "system": {
                "device": "auto",
                "precision": "fp32",
                "backend": "onnx",
                "threads": 4,
                "log_level": "INFO"
            },
            "image": {
                "clahe": {"clip_limit": 2.0, "tile_grid_size": [8, 8]},
                "white_balance": {"method": "gray_world"},
                "sharpen": {"strength": 1.0, "radius": 1},
                "denoise": {"h": 10.0, "template_window_size": 7, "search_window_size": 21}
            },
            "video": {
                "stabilization": {
                    "smoothing_radius": 30,
                    "border_mode": "reflect",
                    "max_corners": 200,
                    "quality_level": 0.01,
                    "min_distance": 30.0,
                    "rolling_shutter_compensation": True
                },
                "interpolation": {
                    "engine": "rife",
                    "scale_factor": 2
                },
                "scene_detection": {
                    "threshold": 30.0
                }
            },
            "ai": {
                "super_resolution": {
                    "model": "real-esrgan",
                    "scale": 4,
                    "tile_size": 512,
                    "tile_pad": 10
                },
                "denoise": {
                    "model": "dncnn",
                    "strength": 0.1
                }
            }
        }

    def load(self, config_path: str) -> None:
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
            self._update_dict(self.config, user_config)

    def _update_dict(self, target: Dict[str, Any], source: Dict[str, Any]) -> None:
        for k, v in source.items():
            if isinstance(v, dict) and k in target and isinstance(target[k], dict):
                self._update_dict(target[k], v)
            else:
                target[k] = v

    def get(self, key_path: str, default: Any = None) -> Any:
        keys = key_path.split(".")
        curr = self.config
        for k in keys:
            if isinstance(curr, dict) and k in curr:
                curr = curr[k]
            else:
                return default
        return curr

    def set(self, key_path: str, value: Any) -> None:
        keys = key_path.split(".")
        curr = self.config
        for k in keys[:-1]:
            if k not in curr or not isinstance(curr[k], dict):
                curr[k] = {}
            curr = curr[k]
        curr[keys[-1]] = value
