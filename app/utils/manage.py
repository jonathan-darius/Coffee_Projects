import warnings
from typing import Awaitable, Callable, Union
from fastapi_login import utils


def user_loader(self, *args, **kwargs) -> Union[Callable, Awaitable]:
    def decorator(callback: Union[Callable, Awaitable]):
        self._user_callback = utils.ordered_partial(callback, *args, **kwargs)
        return callback

    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        fn = args[0]
        args = ()
        warnings.warn(
            SyntaxWarning(
                "As of version 1.7.0 decorating your callback like this is not recommended anymore.\n"
                "Please add empty parentheses like this @manager.user_loader() if you don't "
                "wish to pass additional arguments to your callback."
            )
        )

        decorator(fn)
        return fn

    return decorator
