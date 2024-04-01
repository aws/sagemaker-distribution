import pandas, sys, os, site

# We change the working directory here because there is at least one test (`test_html_template_extends_options`) which
# expects the directory to be 'pandas'. Ideally, we would have changed directories through a `WORKDIR` in Dockerfile
# but unfortunately it doesn't accept dynamic arguments.
site_packages_dir = site.getsitepackages()[0]
os.chdir(site_packages_dir)

# pandas.test() by default runs with `-m "not slow and not network and not db"`. However, we found a few tests in the
# test_network.py file that should have been marked as "network" but weren't, so we skip those here. We skip S3 specific
# tests for the same reason.
# We skip `test_plain_axes` too: the Pandas dev environment expects matplotlib to be ">=3.6.1, <3.7.0" but the runtime
# expectation is just ">=3.6.1". Our image contains v3.7.1, so it meets the latter requirement but not the former. This
# particular test, however, only works with the former requirement. (We verified that the test succeeds if we manually
# drop the version to v3.6.x) So, we skip it.
# Also skipping specific TestFrameFlexArithmetic test; failing due to known issue https://github.com/pandas-dev/pandas/issues/54546
tests_succeeded = pandas.test(
    [
        "-m",
        "(not slow and not network and not db)",
        "-k",
        "(not test_network and not s3 and not test_plain_axes)",
        "--no-strict-data-files",
        "--ignore",
        "pandas/tests/frame/test_arithmetic.py::TestFrameFlexArithmetic::test_floordiv_axis0_numexpr_path",
    ]
)

sys.exit(not tests_succeeded)
