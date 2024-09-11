from dishka import AsyncContainer

from logic.init import _init_container


def init_dummy_container() -> AsyncContainer:
    contaner = _init_container()

    return contaner

