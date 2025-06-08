import os
import tomli
# import tomllib


class ConfigReader(object):
    def __init__(self, key_delimiter="."):
        self._config = {}

        self._key_delimiter = key_delimiter
        self._config_path = os.path.join(os.getcwd(), "config")

        self._config_name = os.getenv("APP_ENV") or "dev"
        self._config_file = f"{self._config_name}.toml"

        self._env_prefix = "BETA_USERS_AI_TESTER"

    def _get_env_config_file(self):
        return os.path.join(self._config_path, self._config_file)

    def _merge_dicts(self, src, target):
        for k, v in src.items():
            if isinstance(v, dict) and k in target:
                self._merge_dicts(v, target[k])
            else:
                target[k] = v

    def _merge_with_env_prefix(self, key):
        key = key.replace(".", "_")

        if self._env_prefix != "":
            return f"{self._env_prefix}_{key}".upper()

        return key.upper()

    def _search_dict(self, d, keys):
        if not keys:
            return d
        for key in keys:
            val = self._find_insensitive(key, d)
            if val is not None and not isinstance(val, dict):
                return val
            elif val:
                return self._search_dict(val, keys[1::])
            else:
                return None

    def _find_insensitive(self, key, source):
        real_key = next((real for real in source.keys() if real.lower() == key.lower()), None)
        return source.get(real_key)

    def get(self, key):
        # Read from ENV first
        val = os.getenv(self._merge_with_env_prefix(key))
        if val is not None:
            return val

        # Check from handlers (env + default)
        val = self._find_insensitive(key, self._config)
        if val is not None:
            return val

        # Find nested handlers parameter
        if self._key_delimiter in key:
            path = key.split(self._key_delimiter)

            source = self.get(path[0])
            if source is not None and isinstance(source, dict):
                val = self._search_dict(source, path[1::])
                if val is not None:
                    return val

        return None

    def read_config(self):
        cfg = {}
        self._config = {}

        with open(self._get_env_config_file()) as fp:
            f = fp.read()
            cfg.update(tomli.loads(f))
            # cfg.update(tomllib.loads(f))

        self._merge_dicts(cfg, self._config)

        return self
