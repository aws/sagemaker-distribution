import os
import site
import sys

import pandas

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
# Also skipping clipboard tests.The tests require pyqt dependency which is missing from SMD images.
tests_succeeded = pandas.test(
    [
        "-m",
        "(not slow and not network and not db and not clipboard)",
        "-k",
        "(not test_network and not s3 and not test_plain_axes and not test_xsqlite_execute_closed_connection and not test_sql"
        # pyarrow's bundled tz database no longer has legacy aliases like US/Pacific and US/Eastern.
        " and not test_from_sequence_of_strings_pa_array and not test_dt_tz_localize and not test_parsing_tzlocal_deprecated"
        # matplotlib >=3.11 changed default prop-cycle colors from hex strings to RGB tuples, and changed gridspec /
        # minor-tick / pie-label / converter-registration behaviour that these pandas 2.3 plotting tests assert on.
        " and not test_default_colors_named_undefined_prop_cycle and not test_colors_in_theme"
        " and not test_df_gridspec_patterns_vert_horiz and not test_df_gridspec_patterns_boxed"
        " and not test_df_subplots_patterns_minorticks_1st_ax_hidden and not test_pandas_plots_register"
        " and not test_pie_series_autopct_and_fontsize"
        # data7 builds datetimes with a pytz "CET" tzinfo; with the image's tz database the LMT offset no longer matches.
        " and not test_array_inference)",
        "-W",
        "ignore::PendingDeprecationWarning",
        # pandas 2.3 plotting still reads Locator.locs, deprecated in matplotlib 3.11; pandas' config turns it into an error.
        "-W",
        "ignore::matplotlib._api.deprecation.MatplotlibDeprecationWarning",
        "--no-strict-data-files",
        "--ignore",
        "pandas/tests/frame/test_arithmetic.py::TestFrameFlexArithmetic::test_floordiv_axis0_numexpr_path",
    ]
)

sys.exit(not tests_succeeded)
