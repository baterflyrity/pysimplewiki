from toml import load

from engine.path import Path

with open(Path.cwd() / 'config.toml', 'r', encoding='utf8') as f:
	settings = load(f)
