import numpy as np

from src.core.local_native_methods import LocalNativeMethods

def run_threshold(src: np.ndarray, threshold: int) -> np.ndarray:
    """Convenience wrapper around the native threshold routine."""
    src = np.ascontiguousarray(src, dtype=np.uint8)
    dst = np.empty_like(src)

    LocalNativeMethods.stvision.threshold(
        src.ctypes.data,
        dst.ctypes.data,
        src.size,
        threshold,
    )

    return dst


def numpy_threshold(src: np.ndarray, threshold: int) -> np.ndarray:
    """Reference implementation."""
    return np.where(src > threshold, 0x80, 0).astype(np.uint8)


def test_threshold_matches_numpy_regression_simd_mask():
    """
    Regression test for the SIMD XOR-mask construction bug.

    The previous implementation generated:

        FF 80 FF 80 ...

    instead of:

        80 80 80 80 ...

    causing every other SIMD lane to disagree with NumPy.
    """
    threshold = 245

    # One full SIMD register.
    src = np.full(16, 246, dtype=np.uint8)

    expected = numpy_threshold(src, threshold)
    actual = run_threshold(src, threshold)

    np.testing.assert_array_equal(actual, expected)


def test_threshold_boundary():
    """Verify the comparison is strictly greater-than."""
    src = np.array(
        [244, 245, 246, 247],
        dtype=np.uint8,
    )

    expected = np.array(
        [0x00, 0x00, 0x80, 0x80],
        dtype=np.uint8,
    )

    actual = run_threshold(src, 245)

    np.testing.assert_array_equal(actual, expected)


def test_threshold_matches_numpy_exactly_one_simd_register():
    """Exercise every SIMD lane exactly once."""
    threshold = 245

    src = np.arange(240, 256, dtype=np.uint8)

    expected = numpy_threshold(src, threshold)
    actual = run_threshold(src, threshold)

    np.testing.assert_array_equal(actual, expected)


def test_threshold_matches_numpy_multiple_registers():
    """Verify correctness across multiple SIMD iterations."""
    rng = np.random.default_rng(12345)

    src = rng.integers(
        0,
        256,
        size=16 * 8,
        dtype=np.uint8,
    )

    threshold = 173

    expected = numpy_threshold(src, threshold)
    actual = run_threshold(src, threshold)

    np.testing.assert_array_equal(actual, expected)


def test_threshold_matches_numpy_with_tail_bytes():
    """Exercise both the SIMD loop and scalar tail path."""
    rng = np.random.default_rng(67890)

    # 16 + 7 bytes
    src = rng.integers(
        0,
        256,
        size=23,
        dtype=np.uint8,
    )

    threshold = 80

    expected = numpy_threshold(src, threshold)
    actual = run_threshold(src, threshold)

    np.testing.assert_array_equal(actual, expected)


def test_threshold_outputs_only_00_or_80():
    """
    The implementation should never emit 0xFF.

    A broken SIMD compare mask previously produced alternating 0xFF bytes.
    """
    rng = np.random.default_rng(42)

    src = rng.integers(
        0,
        256,
        size=1024,
        dtype=np.uint8,
    )

    actual = run_threshold(src, 127)

    unique = np.unique(actual)

    np.testing.assert_array_equal(
        unique,
        np.array([0x00, 0x80], dtype=np.uint8),
    )


def test_threshold_matches_numpy_many_thresholds():
    """Compare against NumPy over several representative thresholds."""
    rng = np.random.default_rng(999)

    src = rng.integers(
        0,
        256,
        size=257,
        dtype=np.uint8,
    )

    for threshold in (0, 1, 80, 127, 128, 245, 254, 255):
        expected = numpy_threshold(src, threshold)
        actual = run_threshold(src, threshold)

        np.testing.assert_array_equal(actual, expected)