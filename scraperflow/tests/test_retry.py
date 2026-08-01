import pytest
from unittest.mock import patch
from scraperflow.retry import retry
from scraperflow.exceptions import TransientFetchError, PermanentFetchError


def make_flaky(fail_count, exception=TransientFetchError("transient")):
    """Returns a function that fails fail_count times then succeeds."""
    calls = [0]
    def fn():
        calls[0] += 1
        if calls[0] <= fail_count:
            raise exception
        return "ok"
    return fn, calls


class TestRetryDecorator:

    def test_succeeds_on_first_attempt(self):
        fn, calls = make_flaky(0)
        decorated = retry(max_attempts=3)(fn)
        with patch("scraperflow.retry.time.sleep") as mock_sleep:
            result = decorated()
        assert result == "ok"
        assert calls[0] == 1
        mock_sleep.assert_not_called()

    def test_succeeds_after_transient_failure(self):
        fn, calls = make_flaky(2)
        decorated = retry(max_attempts=3)(fn)
        with patch("scraperflow.retry.time.sleep") as mock_sleep:
            result = decorated()
        assert result == "ok"
        assert calls[0] == 3
        assert mock_sleep.call_count == 2

    def test_exhausts_max_attempts(self):
        fn, calls = make_flaky(10)
        decorated = retry(max_attempts=3)(fn)
        with patch("scraperflow.retry.time.sleep"):
            with pytest.raises(TransientFetchError):
                decorated()
        assert calls[0] == 3

    def test_does_not_catch_permanent_error(self):
        fn, calls = make_flaky(1, PermanentFetchError("permanent"))
        decorated = retry(max_attempts=3)(fn)
        with patch("scraperflow.retry.time.sleep") as mock_sleep:
            with pytest.raises(PermanentFetchError):
                decorated()
        assert calls[0] == 1
        mock_sleep.assert_not_called()

    def test_does_not_catch_unexpected_error(self):
        fn, calls = make_flaky(1, ValueError("bug"))
        decorated = retry(max_attempts=3)(fn)
        with patch("scraperflow.retry.time.sleep") as mock_sleep:
            with pytest.raises(ValueError):
                decorated()
        assert calls[0] == 1
        mock_sleep.assert_not_called()

    def test_backoff_with_jitter(self):
        fn, _ = make_flaky(4)
        decorated = retry(max_attempts=5, base_delay=1.0)(fn)
        with patch("scraperflow.retry.time.sleep") as mock_sleep:
            decorated()
        delays = [call.args[0] for call in mock_sleep.call_args_list]
        assert len(delays) == 4
        # Delays should be non-negative and within exponential ceiling
        for i, d in enumerate(delays):
            assert 0 <= d <= 1.0 * (2 ** i)
        # Jitter means not all delays are identical
        assert len(set(delays)) > 1

    def test_preserves_function_metadata(self):
        def my_func():
            """My docstring."""
            pass
        decorated = retry(max_attempts=3)(my_func)
        assert decorated.__name__ == "my_func"
        assert decorated.__doc__ == "My docstring."
