"""
Tests for /ES and /NQ option symbol generation.

Validates the OptionSymbolBuilder produces correct TOS RTD option symbols
for various expiration types: weekly (Mon-Fri), monthly (3rd Friday),
end-of-month, and quarterly expirations.

Symbol format reference (TOS RTD):
  /ES options:
    Weekly Mon-Thu:  ./E{week}{weekday}{month}{year}C{strike}:XCME
    Weekly Friday:   ./EW{week}{month}{year}C{strike}:XCME
    EOM:             ./EW{month}{year}C{strike}:XCME
    Quarterly AM:    ./ES{month}{year}C{strike}:XCME
    Quarterly PM:    ./EW{month}{year}C{strike}:XCME

  /NQ options:
    Weekly Mon-Thu:  ./Q{week}{weekday}{month}{year}C{strike}:XCME
    Weekly Friday:   ./QN{week}{month}{year}C{strike}:XCME
    EOM:             ./QNE{month}{year}C{strike}:XCME
    Quarterly AM:    ./NQ{month}{year}C{strike}:XCME
    Quarterly PM:    ./QN{week}{month}{year}C{strike}:XCME

  Weekday codes: A=Mon, B=Tue, C=Wed, D=Thu, W=Fri
  Month codes:   F=Jan, G=Feb, H=Mar, J=Apr, K=May, M=Jun,
                 N=Jul, Q=Aug, U=Sep, V=Oct, X=Nov, Z=Dec
"""

import pytest
from datetime import date
from src.utils.option_symbol_builder import OptionSymbolBuilder


# ---------------------------------------------------------------------------
# Helper: extract product codes from built symbols (without strike/exchange)
# ---------------------------------------------------------------------------
def _extract_product_codes(symbols: list) -> set:
    """Extract unique product code prefixes from generated symbols."""
    codes = set()
    for sym in symbols:
        # Strip leading "./"
        s = sym.lstrip("./")
        # Remove exchange suffix
        s = s.split(":")[0]
        # Remove everything from C or P onward (strike)
        for marker in ("C", "P"):
            idx = s.find(marker)
            if idx > 0:
                codes.add(s[:idx])
                break
    return codes


# ===================================================================
# _is_third_friday
# ===================================================================
class TestIsThirdFriday:
    def test_third_friday_jan_2025(self):
        assert OptionSymbolBuilder._is_third_friday(date(2025, 1, 17)) is True

    def test_not_third_friday(self):
        assert OptionSymbolBuilder._is_third_friday(date(2025, 1, 10)) is False

    def test_third_friday_mar_2025(self):
        assert OptionSymbolBuilder._is_third_friday(date(2025, 3, 21)) is True

    def test_third_friday_jun_2025(self):
        assert OptionSymbolBuilder._is_third_friday(date(2025, 6, 20)) is True

    def test_third_friday_sep_2025(self):
        assert OptionSymbolBuilder._is_third_friday(date(2025, 9, 19)) is True

    def test_third_friday_dec_2025(self):
        assert OptionSymbolBuilder._is_third_friday(date(2025, 12, 19)) is True

    def test_third_friday_mar_2026(self):
        assert OptionSymbolBuilder._is_third_friday(date(2026, 3, 20)) is True

    def test_fourth_friday_not_third(self):
        assert OptionSymbolBuilder._is_third_friday(date(2025, 1, 24)) is False


# ===================================================================
# _is_end_of_month  (fixed to handle weekends)
# ===================================================================
class TestIsEndOfMonth:
    def test_last_weekday_jan_2025(self):
        # Jan 31, 2025 is Friday - last business day
        assert OptionSymbolBuilder._is_end_of_month(date(2025, 1, 31)) is True

    def test_not_last_weekday(self):
        assert OptionSymbolBuilder._is_end_of_month(date(2025, 1, 30)) is False

    def test_last_weekday_feb_2025(self):
        # Feb 28, 2025 is Friday - last business day
        assert OptionSymbolBuilder._is_end_of_month(date(2025, 2, 28)) is True

    def test_month_ending_on_saturday(self):
        # Nov 2025: Nov 30 is Sunday, last business day is Nov 28 (Friday)
        assert OptionSymbolBuilder._is_end_of_month(date(2025, 11, 28)) is True
        assert OptionSymbolBuilder._is_end_of_month(date(2025, 11, 30)) is False

    def test_month_ending_on_sunday(self):
        # Aug 2025: Aug 31 is Sunday, last business day is Aug 29 (Friday)
        assert OptionSymbolBuilder._is_end_of_month(date(2025, 8, 29)) is True
        assert OptionSymbolBuilder._is_end_of_month(date(2025, 8, 31)) is False

    def test_march_2025_last_business_day(self):
        # March 31, 2025 is Monday - it IS the last business day
        assert OptionSymbolBuilder._is_end_of_month(date(2025, 3, 31)) is True

    def test_april_2025_last_business_day(self):
        # April 30, 2025 is Wednesday
        assert OptionSymbolBuilder._is_end_of_month(date(2025, 4, 30)) is True

    def test_june_2025_last_business_day(self):
        # June 30, 2025 is Monday
        assert OptionSymbolBuilder._is_end_of_month(date(2025, 6, 30)) is True

    def test_sep_2026_last_business_day(self):
        # Sep 30, 2026 is Wednesday
        assert OptionSymbolBuilder._is_end_of_month(date(2026, 9, 30)) is True


# ===================================================================
# _is_quarterly_expiration
# ===================================================================
class TestIsQuarterlyExpiration:
    def test_quarterly_mar_2025(self):
        assert OptionSymbolBuilder._is_quarterly_expiration(date(2025, 3, 21)) is True

    def test_quarterly_jun_2025(self):
        assert OptionSymbolBuilder._is_quarterly_expiration(date(2025, 6, 20)) is True

    def test_quarterly_sep_2025(self):
        assert OptionSymbolBuilder._is_quarterly_expiration(date(2025, 9, 19)) is True

    def test_quarterly_dec_2025(self):
        assert OptionSymbolBuilder._is_quarterly_expiration(date(2025, 12, 19)) is True

    def test_not_quarterly_jan(self):
        # Jan is not a quarterly month
        assert OptionSymbolBuilder._is_quarterly_expiration(date(2025, 1, 17)) is False

    def test_not_quarterly_wrong_friday(self):
        # 2nd Friday of March, not 3rd
        assert OptionSymbolBuilder._is_quarterly_expiration(date(2025, 3, 14)) is False


# ===================================================================
# _get_week_indicator
# ===================================================================
class TestGetWeekIndicator:
    def test_first_friday_jan_2025(self):
        # Jan 3, 2025 = first Friday
        assert OptionSymbolBuilder._get_week_indicator(date(2025, 1, 3)) == "1"

    def test_second_friday_jan_2025(self):
        assert OptionSymbolBuilder._get_week_indicator(date(2025, 1, 10)) == "2"

    def test_third_friday_jan_2025(self):
        assert OptionSymbolBuilder._get_week_indicator(date(2025, 1, 17)) == "3"

    def test_fourth_friday_jan_2025(self):
        assert OptionSymbolBuilder._get_week_indicator(date(2025, 1, 24)) == "4"

    def test_fifth_friday_jan_2025(self):
        assert OptionSymbolBuilder._get_week_indicator(date(2025, 1, 31)) == "5"

    def test_monday_week2(self):
        # Jan 6 (Monday) belongs to week 2 (same week as Jan 10 Friday)
        assert OptionSymbolBuilder._get_week_indicator(date(2025, 1, 6)) == "2"

    def test_wednesday_week1(self):
        # Jan 1 (Wednesday) belongs to week 1 (same week as Jan 3 Friday)
        assert OptionSymbolBuilder._get_week_indicator(date(2025, 1, 1)) == "1"

    def test_month_starting_saturday(self):
        # Feb 2025: Feb 1 is Saturday, first business day is Feb 3 (Monday)
        # Feb 3 Monday -> week 1 (Friday Feb 7)
        assert OptionSymbolBuilder._get_week_indicator(date(2025, 2, 3)) == "1"
        assert OptionSymbolBuilder._get_week_indicator(date(2025, 2, 7)) == "1"
        assert OptionSymbolBuilder._get_week_indicator(date(2025, 2, 10)) == "2"

    def test_month_starting_friday(self):
        # Aug 2025: Aug 1 is Friday
        assert OptionSymbolBuilder._get_week_indicator(date(2025, 8, 1)) == "1"
        assert OptionSymbolBuilder._get_week_indicator(date(2025, 8, 4)) == "2"
        assert OptionSymbolBuilder._get_week_indicator(date(2025, 8, 8)) == "2"


# ===================================================================
# /ES product codes  (_get_es_product_code)
# ===================================================================
class TestESProductCode:
    """Test /ES option product code generation."""

    def test_weekly_friday(self):
        # Jan 10, 2025 = 2nd Friday, not quarterly, not EOM
        codes = OptionSymbolBuilder._get_es_product_code(date(2025, 1, 10))
        assert codes == ["EW2F25"]

    def test_weekly_monday(self):
        # Jan 6, 2025 = Monday of week 2
        codes = OptionSymbolBuilder._get_es_product_code(date(2025, 1, 6))
        assert codes == ["E2AF25"]

    def test_weekly_tuesday(self):
        # Jan 7, 2025 = Tuesday of week 2
        codes = OptionSymbolBuilder._get_es_product_code(date(2025, 1, 7))
        assert codes == ["E2BF25"]

    def test_weekly_wednesday(self):
        # Jan 8, 2025 = Wednesday of week 2
        codes = OptionSymbolBuilder._get_es_product_code(date(2025, 1, 8))
        assert codes == ["E2CF25"]

    def test_weekly_thursday(self):
        # Jan 9, 2025 = Thursday of week 2
        codes = OptionSymbolBuilder._get_es_product_code(date(2025, 1, 9))
        assert codes == ["E2DF25"]

    def test_eom_jan_2025(self):
        # Jan 31, 2025 = Friday, last business day (EOM)
        codes = OptionSymbolBuilder._get_es_product_code(date(2025, 1, 31))
        assert codes == ["EWF25"]

    def test_quarterly_mar_2025(self):
        # Mar 21, 2025 = 3rd Friday, quarterly
        codes = OptionSymbolBuilder._get_es_product_code(date(2025, 3, 21))
        assert "ESH25" in codes  # AM settled
        assert "EWH25" in codes  # PM settled

    def test_quarterly_jun_2025(self):
        codes = OptionSymbolBuilder._get_es_product_code(date(2025, 6, 20))
        assert "ESM25" in codes
        assert "EWM25" in codes

    def test_quarterly_sep_2025(self):
        codes = OptionSymbolBuilder._get_es_product_code(date(2025, 9, 19))
        assert "ESU25" in codes
        assert "EWU25" in codes

    def test_quarterly_dec_2025(self):
        codes = OptionSymbolBuilder._get_es_product_code(date(2025, 12, 19))
        assert "ESZ25" in codes
        assert "EWZ25" in codes

    def test_eom_when_month_ends_weekend(self):
        # Nov 28, 2025 = Friday, last business day (Nov 30 is Sunday)
        codes = OptionSymbolBuilder._get_es_product_code(date(2025, 11, 28))
        assert codes == ["EWX25"]

    def test_weekly_friday_week4(self):
        # Jan 24, 2025 = 4th Friday
        codes = OptionSymbolBuilder._get_es_product_code(date(2025, 1, 24))
        assert codes == ["EW4F25"]

    def test_non_quarterly_third_friday(self):
        # Jan 17, 2025 = 3rd Friday of Jan (non-quarterly month)
        codes = OptionSymbolBuilder._get_es_product_code(date(2025, 1, 17))
        assert codes == ["EW3F25"]

    def test_eom_march_not_quarterly(self):
        # Mar 31, 2025 = Monday, last business day. NOT quarterly (quarterly is 3rd Fri)
        codes = OptionSymbolBuilder._get_es_product_code(date(2025, 3, 31))
        assert codes == ["EWH25"]


# ===================================================================
# /NQ product codes  (_get_nq_product_code)
# ===================================================================
class TestNQProductCode:
    """Test /NQ option product code generation."""

    def test_weekly_friday(self):
        # Jan 10, 2025 = 2nd Friday
        codes = OptionSymbolBuilder._get_nq_product_code(date(2025, 1, 10))
        assert codes == ["QN2F25"]

    def test_weekly_monday(self):
        # Jan 6, 2025 = Monday of week 2
        codes = OptionSymbolBuilder._get_nq_product_code(date(2025, 1, 6))
        assert codes == ["Q2AF25"]

    def test_weekly_tuesday(self):
        codes = OptionSymbolBuilder._get_nq_product_code(date(2025, 1, 7))
        assert codes == ["Q2BF25"]

    def test_weekly_wednesday(self):
        codes = OptionSymbolBuilder._get_nq_product_code(date(2025, 1, 8))
        assert codes == ["Q2CF25"]

    def test_weekly_thursday(self):
        codes = OptionSymbolBuilder._get_nq_product_code(date(2025, 1, 9))
        assert codes == ["Q2DF25"]

    def test_eom_jan_2025(self):
        # Jan 31 = last business day
        codes = OptionSymbolBuilder._get_nq_product_code(date(2025, 1, 31))
        assert codes == ["QNEF25"]

    def test_quarterly_mar_2025(self):
        codes = OptionSymbolBuilder._get_nq_product_code(date(2025, 3, 21))
        assert "NQH25" in codes  # AM settled
        # PM settled should be QN{week}H25
        pm_codes = [c for c in codes if c.startswith("QN")]
        assert len(pm_codes) == 1
        assert pm_codes[0] == "QN3H25"

    def test_quarterly_jun_2025(self):
        codes = OptionSymbolBuilder._get_nq_product_code(date(2025, 6, 20))
        assert "NQM25" in codes
        pm_codes = [c for c in codes if c.startswith("QN")]
        assert len(pm_codes) == 1
        assert pm_codes[0] == "QN3M25"

    def test_quarterly_sep_2025(self):
        codes = OptionSymbolBuilder._get_nq_product_code(date(2025, 9, 19))
        assert "NQU25" in codes

    def test_quarterly_dec_2025(self):
        codes = OptionSymbolBuilder._get_nq_product_code(date(2025, 12, 19))
        assert "NQZ25" in codes

    def test_eom_when_month_ends_weekend(self):
        # Aug 29, 2025 = Friday, last business day (Aug 31 is Sunday)
        codes = OptionSymbolBuilder._get_nq_product_code(date(2025, 8, 29))
        assert codes == ["QNEQ25"]

    def test_nq_string_no_spaces(self):
        """Regression: quarterly PM code must not have spaces or '+'."""
        codes = OptionSymbolBuilder._get_nq_product_code(date(2025, 3, 21))
        for code in codes:
            assert " " not in code, f"Space found in code: {code!r}"
            assert "+" not in code, f"Plus found in code: {code!r}"

    def test_eom_march(self):
        # Mar 31, 2025 = Monday, EOM
        codes = OptionSymbolBuilder._get_nq_product_code(date(2025, 3, 31))
        assert codes == ["QNEH25"]

    def test_non_quarterly_third_friday(self):
        # Jan 17 = 3rd Friday of non-quarterly month
        codes = OptionSymbolBuilder._get_nq_product_code(date(2025, 1, 17))
        assert codes == ["QN3F25"]


# ===================================================================
# build_symbols integration tests
# ===================================================================
class TestBuildSymbolsES:
    """Integration tests for /ES symbol building."""

    def test_basic_es_weekly_friday(self):
        symbols = OptionSymbolBuilder.build_symbols(
            "/ES", date(2025, 1, 10), 5900.0, 10, 5.0
        )
        assert len(symbols) > 0
        # All should be XCME exchange
        for s in symbols:
            assert s.endswith(":XCME")
        # Should contain calls and puts
        calls = [s for s in symbols if "C" in s.split(":")[0]]
        puts = [s for s in symbols if "P" in s.split(":")[0]]
        assert len(calls) > 0
        assert len(puts) > 0
        # Product code should be EW2F25
        codes = _extract_product_codes(symbols)
        assert "EW2F25" in codes

    def test_es_quarterly(self):
        symbols = OptionSymbolBuilder.build_symbols(
            "/ES", date(2025, 3, 21), 5900.0, 10, 5.0
        )
        codes = _extract_product_codes(symbols)
        assert "ESH25" in codes
        assert "EWH25" in codes

    def test_es_eom(self):
        symbols = OptionSymbolBuilder.build_symbols(
            "/ES", date(2025, 1, 31), 5900.0, 10, 5.0
        )
        codes = _extract_product_codes(symbols)
        assert "EWF25" in codes

    def test_es_symbol_format(self):
        """Verify individual symbol format: ./{code}C{strike}:XCME"""
        symbols = OptionSymbolBuilder.build_symbols(
            "/ES", date(2025, 1, 10), 5900.0, 5, 5.0
        )
        for sym in symbols:
            assert sym.startswith("./"), f"Symbol should start with './': {sym}"
            assert ":XCME" in sym, f"Symbol should contain ':XCME': {sym}"


class TestBuildSymbolsNQ:
    """Integration tests for /NQ symbol building."""

    def test_basic_nq_weekly_friday(self):
        symbols = OptionSymbolBuilder.build_symbols(
            "/NQ", date(2025, 1, 10), 21000.0, 50, 25.0
        )
        assert len(symbols) > 0
        codes = _extract_product_codes(symbols)
        assert "QN2F25" in codes

    def test_nq_quarterly(self):
        symbols = OptionSymbolBuilder.build_symbols(
            "/NQ", date(2025, 3, 21), 21000.0, 50, 25.0
        )
        codes = _extract_product_codes(symbols)
        assert "NQH25" in codes

    def test_nq_quarterly_no_malformed_codes(self):
        """Regression: no spaces or '+' in any generated symbol."""
        symbols = OptionSymbolBuilder.build_symbols(
            "/NQ", date(2025, 3, 21), 21000.0, 50, 25.0
        )
        for sym in symbols:
            assert " " not in sym, f"Space in symbol: {sym!r}"
            assert "+" not in sym, f"Plus in symbol: {sym!r}"

    def test_nq_eom(self):
        symbols = OptionSymbolBuilder.build_symbols(
            "/NQ", date(2025, 1, 31), 21000.0, 50, 25.0
        )
        codes = _extract_product_codes(symbols)
        assert "QNEF25" in codes

    def test_nq_monday(self):
        symbols = OptionSymbolBuilder.build_symbols(
            "/NQ", date(2025, 1, 6), 21000.0, 50, 25.0
        )
        codes = _extract_product_codes(symbols)
        assert "Q2AF25" in codes


# ===================================================================
# Edge cases
# ===================================================================
class TestEdgeCases:
    def test_invalid_price(self):
        assert OptionSymbolBuilder.build_symbols("/ES", date(2025, 1, 10), 0, 10, 5.0) == []
        assert OptionSymbolBuilder.build_symbols("/ES", date(2025, 1, 10), -100, 10, 5.0) == []

    def test_invalid_range(self):
        assert OptionSymbolBuilder.build_symbols("/ES", date(2025, 1, 10), 5900, 0, 5.0) == []

    def test_invalid_spacing(self):
        assert OptionSymbolBuilder.build_symbols("/ES", date(2025, 1, 10), 5900, 10, 0) == []

    def test_strike_formatting_whole(self):
        assert OptionSymbolBuilder._format_strike(5900.0, is_futures=True) == "5900"

    def test_strike_formatting_half(self):
        assert OptionSymbolBuilder._format_strike(109.5, is_futures=True, strike_spacing=0.5) == "109.5"

    def test_strike_formatting_quarter(self):
        assert OptionSymbolBuilder._format_strike(109.25, is_futures=True, strike_spacing=0.25) == "109.25"
        assert OptionSymbolBuilder._format_strike(109.75, is_futures=True, strike_spacing=0.25) == "109.75"
        assert OptionSymbolBuilder._format_strike(109.5, is_futures=True, strike_spacing=0.25) == "109.5"
        assert OptionSymbolBuilder._format_strike(110.0, is_futures=True, strike_spacing=0.25) == "110"

    def test_2026_dates(self):
        """Test with dates in 2026 to verify year handling."""
        # Apr 3, 2026 = Friday, week 1
        codes = OptionSymbolBuilder._get_es_product_code(date(2026, 4, 3))
        assert codes == ["EW1J26"]

        codes = OptionSymbolBuilder._get_nq_product_code(date(2026, 4, 3))
        assert codes == ["QN1J26"]

    def test_quarterly_2026(self):
        # Mar 20, 2026 = 3rd Friday of March
        codes = OptionSymbolBuilder._get_es_product_code(date(2026, 3, 20))
        assert "ESH26" in codes

        codes = OptionSymbolBuilder._get_nq_product_code(date(2026, 3, 20))
        assert "NQH26" in codes

    def test_eom_weekend_2026(self):
        # May 2026: May 31 is Sunday, last business day is May 29 (Friday)
        assert OptionSymbolBuilder._is_end_of_month(date(2026, 5, 29)) is True
        codes = OptionSymbolBuilder._get_es_product_code(date(2026, 5, 29))
        assert codes == ["EWK26"]
