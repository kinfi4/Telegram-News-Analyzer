class ConfigReader:
    def __init__(self, config_file_path: str):
        self._file_path = config_file_path

        with open(self._file_path) as conf_file:
            self._file_lines: list = conf_file.readlines()

    def get(self, key: str):
        for line in self._file_lines:
            tokens = line.split('=')

            if len(tokens) == 1 and tokens[0] == key:
                return

            if len(tokens) > 2:
                raise ValueError(f'Line: {line} has a "=" sign in a value, it is forbidden')

            line_key, line_value = tokens
            if line_key == key:
                return line_value.strip()

        raise AttributeError(f'Variable with key: {key} was not found in a config file')

    def set(self, key: str, value: str):
        for index, line in enumerate(self._file_lines):
            line_key, line_value = line.split('=')

            if line_key == key:
                self._file_lines[index] = f'{key}={value}'
                break
        else:
            self._file_lines.append(f'{key}={value}')

        with open(self._file_path, 'w') as conf_file:
            conf_file.writelines(self._file_lines)
