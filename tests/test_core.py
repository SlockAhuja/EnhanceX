import pytest
from enhancex.core.logger import get_logger, set_log_level
from enhancex.core.config import ConfigManager
from enhancex.core.scheduler import TaskScheduler
from enhancex.core.cache import MemoryCache


def test_logger():
    logger = get_logger("TestLogger")
    assert logger is not None
    set_log_level("DEBUG", "TestLogger")
    logger.debug("Test debug message")


def test_config_manager():
    config = ConfigManager.get_instance()
    assert config.get("system.threads") == 4
    config.set("system.threads", 8)
    assert config.get("system.threads") == 8
    assert config.get("nonexistent.key", "default_val") == "default_val"


def test_scheduler():
    scheduler = TaskScheduler(num_workers=2)
    inputs = [1, 2, 3, 4]
    results = scheduler.map(lambda x: x * 2, inputs)
    assert results == [2, 4, 6, 8]
    scheduler.shutdown()


def test_cache():
    cache = MemoryCache(max_size=2)
    cache.put("a", 10)
    cache.put("b", 20)
    assert cache.get("a") == 10
    cache.put("c", 30)  # Evicts LRU 'b' since 'a' was accessed recently
    assert len(cache) == 2
    assert cache.get("b") is None
    cache.clear()
    assert len(cache) == 0
