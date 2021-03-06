"""
This marker is used for purposes of RHV - CFME integration.

Tests can be marked like this:

.. code-block:: python

    @pytest.mark.rhv2
    def test_something():
        assert True

Usage on CLI::

    pytest -m 'rhv1'  # Run only tier 1
    pytest -m 'rhv1 or rhv2 or rhv3'  # Run all the tiers
    pytest -m 'not rhv3'  # Run all test methods except for RHV tier 3
    pytest -m 'not rhv1 and not rhv2 and not rhv3'  # Run everything that is not marked with rhv1-3

To test this module::

    pytest -p pytester markers/rhv.py
"""
RHV_CFME_TIERS = (1, 2, 3)


def pytest_configure(config):
    for tier in RHV_CFME_TIERS:
        config.addinivalue_line("markers", "rhv{t}: Run tier {t} of RHV-CFME tests.".format(t=tier))


def test_rhv_markers(testdir):

    testdir.makepyfile("""
        import pytest

        @pytest.mark.rhv1
        def test_rhv_marker_tier_1():
            assert True

        @pytest.mark.rhv2
        def test_rhv_marker_tier_2():
            assert True

        @pytest.mark.rhv3
        def test_rhv_marker_tier_3():
            assert True

        def test_without_marker():
            assert False
    """)

    testdir.runpytest("-m rhv1", "--strict").assert_outcomes(passed=1)
    testdir.runpytest("-m rhv1 or rhv2 or rhv3", "--strict").assert_outcomes(passed=3)
    testdir.runpytest("-m not rhv3", "--strict").assert_outcomes(passed=2, failed=1)
    testdir.runpytest("-m not rhv1 and not rhv2 and not rhv3", "--strict").assert_outcomes(failed=1)
