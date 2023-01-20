from eventing.event import Event


class EventBus:

    def __init__(self) -> None:
        self._map = {}

    def post(self, event: Event):
        for handler in self._map[event.get_type()]:
            handler()

    def register(self, event_type, handler):
        if event_type not in self._map:
            self._map[event_type] = [handler]
        else:
            self._map[event_type].append(handler)

    def deregister(self, handler):
        for handlers in self._map.values():
            if handler in handlers:
                handlers.remove(handler)
