from typing import Any


class NamespacedCache:
    """缓存管理器

    管理所有Cache实例，提供创建和获取Cache的功能
    """

    def __init__(self):
        """初始化缓存管理器"""
        # 存储所有创建的Cache实例
        self._caches: dict[str, "Cache"] = {}

    def new(self, key: str) -> "Cache":
        """创建或获取一个Cache实例

        如果指定key的Cache已存在，则返回已有实例
        否则创建一个新的Cache实例

        参数:
            key: 缓存标识符

        返回:
            Cache实例
        """
        if key not in self._caches:
            self._caches[key] = Cache(key)
        return self._caches[key]

    def get_cache(self, key: str) -> "Cache | None":
        """获取指定key的Cache实例

        参数:
            key: 缓存标识符

        返回:
            Cache实例，如果不存在则返回None
        """
        return self._caches.get(key)

    def delete_cache(self, key: str) -> None:
        """删除指定key的Cache实例

        参数:
            key: 缓存标识符
        """
        if key in self._caches:
            del self._caches[key]

    def clear_all(self) -> None:
        """清空所有Cache实例"""
        for cache in self._caches.values():
            cache.clear()

    def get_all_keys(self) -> list[str]:
        """获取所有Cache的key列表

        返回:
            所有Cache的key列表
        """
        return list(self._caches.keys())


class Cache:
    """普通缓存类

    提供简单的键值存储接口
    """

    def __init__(self, name: str):
        """初始化缓存

        参数:
            name: 缓存名称
        """
        self._name = name
        self._cache: dict[str, Any] = {}

    @property
    def name(self) -> str:
        """获取缓存名称"""
        return self._name

    def get(self, key: str) -> Any:
        """获取缓存值

        参数:
            key: 缓存键

        返回:
            缓存值，不存在则返回None
        """
        return self._cache.get(key)

    def set(self, key: str, value: Any) -> None:
        """设置缓存值

        参数:
            key: 缓存键
            value: 缓存值
        """
        self._cache[key] = value

    def delete(self, key: str) -> None:
        """删除缓存项

        参数:
            key: 缓存键
        """
        if key in self._cache:
            del self._cache[key]

    def clear(self) -> None:
        """清空所有缓存"""
        self._cache.clear()

    def has_key(self, key: str) -> bool:
        """检查是否存在某个键

        参数:
            key: 缓存键

        返回:
            是否存在该键
        """
        return key in self._cache

    def get_all(self) -> dict[str, Any]:
        """获取所有缓存数据

        返回:
            所有缓存数据字典
        """
        return self._cache.copy()

    def __len__(self) -> int:
        """返回缓存中的项目数量"""
        return len(self._cache)


# 创建全局缓存管理器实例
cache_root = NamespacedCache()


token_cache = cache_root.new("request_token")
