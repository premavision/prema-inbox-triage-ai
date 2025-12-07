"""Decorators for email provider abstraction between mock and real implementations."""

from __future__ import annotations

import functools
import logging
from typing import Callable, TypeVar, ParamSpec

logger = logging.getLogger(__name__)

P = ParamSpec("P")
R = TypeVar("R")


def mock_fallback(
    mock_func_name: str,
    error_message: str = "Failed to execute real provider, falling back to mock",
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator that wraps a real provider method with mock fallback logic.
    
    If the real method raises an exception, it falls back to the mock implementation.
    The mock function is looked up by name on the instance (self).
    Works with both regular functions and generators.
    
    Args:
        mock_func_name: Name of the mock method on the instance (e.g., "_get_mock_messages")
        error_message: Custom error message to log when falling back
    
    Example:
        @mock_fallback("_get_mock_messages", "Failed to fetch from Gmail API")
        def _list_recent_messages_real(self, *, limit: int = 10):
            # Real Gmail API implementation
    """
    def decorator(real_func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(real_func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                result = real_func(*args, **kwargs)
                # Check if it's a generator (has __iter__ method and is not a string/bytes)
                if hasattr(result, "__iter__") and not isinstance(result, (str, bytes)):
                    # It's a generator, create a wrapper generator
                    def generator_wrapper():
                        try:
                            # Try to yield from the real generator
                            for item in result:
                                yield item
                        except (StopIteration, GeneratorExit):
                            # Normal generator completion, just re-raise
                            raise
                        except Exception as e:
                            logger.warning(f"{error_message}: {type(e).__name__}: {e}")
                            logger.info("Falling back to mock implementation")
                            # Get the instance (first arg should be self)
                            if args:
                                instance = args[0]
                                try:
                                    mock_func = getattr(instance, mock_func_name)
                                    # Yield from mock generator - pass self (args[0]) and remaining args
                                    yield from mock_func(*args, **kwargs)
                                except AttributeError:
                                    logger.error(f"Mock function '{mock_func_name}' not found on instance")
                                    raise
                                except Exception as fallback_error:
                                    logger.error(f"Error in mock fallback: {type(fallback_error).__name__}: {fallback_error}")
                                    raise
                            else:
                                raise
                    return generator_wrapper()  # type: ignore
                return result
            except Exception as e:
                logger.warning(f"{error_message}: {type(e).__name__}: {e}")
                logger.info("Falling back to mock implementation")
                # Get the instance (first arg should be self)
                if args:
                    instance = args[0]
                    try:
                        mock_func = getattr(instance, mock_func_name)
                        # Call mock function with all args (including self)
                        return mock_func(*args, **kwargs)
                    except AttributeError:
                        logger.error(f"Mock function '{mock_func_name}' not found on instance")
                        raise
                    except Exception as fallback_error:
                        logger.error(f"Error in mock fallback: {type(fallback_error).__name__}: {fallback_error}")
                        raise
                raise
        return wrapper
    return decorator


def mock_only(mock_func: Callable[P, R]) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator that ensures a method only runs in mock mode.
    
    If not in mock mode, it raises an error indicating the method should not be called.
    
    Args:
        mock_func: The mock implementation function
    
    Example:
        @mock_only(mock_reset_counter)
        def reset_mock_counter(self):
            # Mock-only implementation
    """
    def decorator(real_func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(real_func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # Check if first argument is self and has settings
            if args and hasattr(args[0], "settings") and hasattr(args[0].settings, "gmail_use_mock"):
                if not args[0].settings.gmail_use_mock:
                    raise ValueError("This method is only available in mock mode")
            return mock_func(*args, **kwargs)
        return wrapper
    return decorator


def conditional_mock(
    condition_func: Callable[[], bool],
    mock_func: Callable[P, R],
    real_func: Callable[P, R],
) -> Callable[P, R]:
    """
    Creates a function that conditionally calls mock or real implementation.
    
    Args:
        condition_func: Function that returns True if mock should be used
        mock_func: Mock implementation
        real_func: Real implementation
    
    Returns:
        A function that calls the appropriate implementation based on condition
    """
    @functools.wraps(real_func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        if condition_func():
            return mock_func(*args, **kwargs)
        return real_func(*args, **kwargs)
    return wrapper
