import pathlib
from .roleinvite import RoleInvite
from redbot.core.data_manager import cog_data_path


def create_cache(cog_path: pathlib.Path):
    if not cog_path.exists():
        return
    path = cog_path / "cache"
    directories = [x for x in cog_path.iterdir() if x.is_dir()]
    if path not in directories:
        path.mkdir()


def create_log(cog_path: pathlib.Path):
    if not cog_path.exists():
        return
    path = cog_path / "logs"
    directories = [x for x in cog_path.iterdir() if x.is_dir()]
    if path not in directories:
        path.mkdir()
        (path / "error.log").touch()
        (path / "debug.log").touch()


def setup(bot):
    n = RoleInvite(bot)
    create_cache(cog_data_path(n))
    create_log(cog_data_path(n))
    bot.add_cog(n)
