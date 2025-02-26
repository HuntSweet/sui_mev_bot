import asyncio
import concurrent.futures
import inspect
import os
from collections import defaultdict
from functools import wraps

ENABLE_SUBSCRIBERS = os.getenv("ASYNC_BUS_ENABLE_SUBSCRIBERS", True)


class EventBus:
    """
    EventBus class to run async subscribers
    """

    def __init__(self, event_loop):
        self.__events_async = defaultdict(set)
        self.__events = defaultdict(set)
        self._pool = concurrent.futures.ThreadPoolExecutor()
        self.event_loop = event_loop

    def __str__(self):
        return "EventBus"

    def __repr__(self):
        event_nums = len(self.__events.items()) + len(self.__events_async.items())
        return f"<EventBus: {event_nums} events>"

    @property
    def events(self):
        """
        Property for returning events and their respective subscribers

        :return: Events and their respective subscribers
        """
        return self.__events

    def subscribe(self, event_name):
        """
        Decorator for subscribing a handler to an event

        :param event_name: Event name for subscribing
        """

        def wrapper(subscriber):
            self.add_event(event_name, subscriber)

            @wraps(subscriber)
            def wrapped(*args, **kwargs):
                return subscriber(*args, **kwargs)

            return wrapped

        return wrapper

    def add_event(self, event_name, subscriber):
        """
        Method for subscribing a handler to an event

        :param event_name: Event name for subscribing
        :param subscriber: Subscriber of the event
        """

        if inspect.iscoroutinefunction(subscriber):
            self.__events_async[event_name].add(subscriber)
        else:
            self.__events[event_name].add(subscriber)

    def emit(self, event_name, *args, **kwargs):
        """
        Method for emitting an event

        :param event_name: Event name for emitting their subscribers
        """
        if ENABLE_SUBSCRIBERS == "false":
            return None

        subscribers = self.__events[event_name]
        subscribers_async = self.__events_async[event_name]

        if subscribers_async and self.event_loop:
            self.event_loop.create_task(
                self.__run_subscribers(subscribers_async, event_name, *args, **kwargs)
            )

        if subscribers:
            self.__run_subscribers_no_async(subscribers, event_name, *args, **kwargs)

    def __run_subscribers_no_async(self, subscribers, event_name, *args, **kwargs):
        # using threads pool to run sync subscribers
        for subscriber in subscribers:
            # thread = threading.Thread(target=subscriber, args=args, kwargs=kwargs)
            # thread.setDaemon(True)
            # thread.start()
            self._pool.submit(subscriber, *args, **kwargs)

    async def __run_subscribers(self, subscribers, event_name, *args, **kwargs):
        await asyncio.wait(
            [
                asyncio.create_task(subscriber(*args, **kwargs))
                for subscriber in subscribers
            ]
        )
