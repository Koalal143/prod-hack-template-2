from dishka import Provider, Scope, provide

from src.config import (
    Settings,
    settings,
)


class ConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def get_settings(self) -> Settings:
        return settings
