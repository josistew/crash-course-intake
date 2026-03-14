"""
build_weekly_report.py — Generates the Rez Weekly Report workbook structure.

Produces: Rez-Weekly-Report.xlsx (saved in the project root)

Usage:
    cd /Users/josi/crash-course-intake
    python3 scripts/build_weekly_report.py

IMPORTANT: Column headers in import tabs are PLACEHOLDERS. After Rez's first
CSV export from each platform, update header rows in each import tab to match
actual column names. Formulas use MATCH() on these headers — they must match
exactly.
"""

import os
import sys

try:
    import openpyxl
    from openpyxl import Workbook
    from openpyxl.styles import (
        Font, PatternFill, Alignment, Border, Side, numbers
    )
    from openpyxl.formatting.rule import CellIsRule
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.datavalidation import DataValidation
    from openpyxl.comments import Comment
except ImportError:
    print("ERROR: openpyxl is required. Install with: pip3 install openpyxl")
    sys.exit(1)

from sample_data import (
    SQUARE_HEADERS, DOORDASH_HEADERS, UBEREATS_HEADERS,
    GRUBHUB_HEADERS, BEK_HEADERS, SQUARE_LABOR_HEADERS,
    LOCATIONS, BRANDS,
    SQUARE_SAMPLE_ROWS, DOORDASH_SAMPLE_ROWS, UBEREATS_SAMPLE_ROWS,
    GRUBHUB_SAMPLE_ROWS, BEK_SAMPLE_ROWS, SQUARE_LABOR_SAMPLE_ROWS,
    EMPLOYEE_ROSTER, PRIOR_WEEK_HEADERS, PRIOR_WEEK_SAMPLE,
)

# ==============================================================================
# OUTPUT PATH
# ==============================================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "Rez-Weekly-Report.xlsx")

# ==============================================================================
# STYLE CONSTANTS
# ==============================================================================

# Tab colors
TAB_IMPORT  = "4A86C8"   # steel blue — import tabs
TAB_CALC    = "999999"   # neutral gray — location calc tabs
TAB_AMBER   = "F4A442"   # amber — Summary + Prior-Week (tabs Rez actually uses)
TAB_GREEN   = "6AA84F"   # sage green — Instructions + Employee-Roster (reference)

# Header background colors
HDR_IMPORT  = "4472C4"   # blue — import tab headers
HDR_CALC    = "2F5496"   # darker blue — calc/summary headers
HDR_INSTR   = "4A86C8"   # same as tab color for Instructions

# Fill colors
FILL_IMPORT_HDR  = PatternFill("solid", fgColor="4472C4")
FILL_CALC_HDR    = PatternFill("solid", fgColor="2F5496")
FILL_INSTR_HDR   = PatternFill("solid", fgColor="2F5496")
FILL_ALT_ROW     = PatternFill("solid", fgColor="F2F2F2")
FILL_WHITE       = PatternFill("solid", fgColor="FFFFFF")
FILL_VALID_BAD   = PatternFill("solid", fgColor="FBE4E4")  # light red — default validation
FILL_VALID_GOOD  = PatternFill("solid", fgColor="D9EAD3")  # light green — OK validation
FILL_MOTO_MEDI   = PatternFill("solid", fgColor="FDE9D9")  # light orange — MM brand band
FILL_TIKKA_SHACK = PatternFill("solid", fgColor="D0E2F1")  # light teal — TS brand band
FILL_AMBER_LIGHT = PatternFill("solid", fgColor="FFF2CC")  # light amber — summary title
FILL_SUMMARY_HDR = PatternFill("solid", fgColor="434343")  # dark — summary column headers

# Fonts
FONT_DEFAULT = Font(name="Calibri", size=11)
FONT_HEADER  = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
FONT_BOLD    = Font(name="Calibri", size=11, bold=True)
FONT_TITLE   = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
FONT_SUMMARY_TITLE = Font(name="Calibri", size=18, bold=True)
FONT_VALID_BAD = Font(name="Calibri", size=10, color="CC0000")
FONT_VALID_OK  = Font(name="Calibri", size=10, color="006100")
FONT_SECTION   = Font(name="Calibri", size=12, bold=True, color="2F5496")

# Alignment
ALIGN_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALIGN_LEFT   = Alignment(horizontal="left",   vertical="center", wrap_text=True)
ALIGN_LEFT_NW = Alignment(horizontal="left",  vertical="top",    wrap_text=True)


def col_width_for(text, padding=4):
    """Return a reasonable column width for the given text plus padding."""
    return max(len(str(text)) + padding, 10)


def style_header_cell(cell, text, fill=None, font=None, alignment=None):
    """Apply bold header styling to a cell."""
    cell.value = text
    cell.font  = font or FONT_HEADER
    cell.fill  = fill or FILL_IMPORT_HDR
    cell.alignment = alignment or ALIGN_CENTER


def apply_tab_color(ws, hex_color):
    ws.sheet_properties.tabColor = hex_color


def freeze(ws, cell_ref):
    ws.freeze_panes = cell_ref


# ==============================================================================
# WORKSHEET BUILDERS
# ==============================================================================

def build_instructions(ws):
    """Build the Instructions tab."""
    apply_tab_color(ws, TAB_GREEN)

    # Title row
    ws.merge_cells("A1:B1")
    cell = ws["A1"]
    cell.value     = "Rez Weekly Report — Instructions"
    cell.font      = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
    cell.fill      = FILL_CALC_HDR
    cell.alignment = ALIGN_CENTER
    ws.row_dimensions[1].height = 30

    # Column A width for readability
    ws.column_dimensions["A"].width = 80
    ws.column_dimensions["B"].width = 20

    rows = [
        # (row_offset_from_current, text, is_section_header)
    ]

    content = [
        ("", False),
        ("IMPORTANT: Column headers in each import tab are PLACEHOLDERS. After your first "
         "CSV export from each platform, update the header row in each import tab to match "
         "your actual column names. The formulas use MATCH() on these headers — they must "
         "match exactly.", False),
        ("", False),
        ("WEEKLY CADENCE", True),
        ("Every Monday morning: clear last week's data from each import tab (delete rows 3 "
         "and below — keep rows 1 and 2), paste new CSVs, then check the Summary tab.", False),
        ("", False),
        ("HOW TO EXPORT & PASTE — SQUARE", True),
        ("1. Log into Square Dashboard", False),
        ("2. Go to: Reports > Sales Summary", False),
        ("3. Select date range: Mon–Sun of the week you are reporting", False),
        ("4. Click 'Export CSV'", False),
        ("5. Open the CSV, select all, copy", False),
        ("6. Click into cell A3 of the Square-Import tab in this workbook", False),
        ("7. Paste (do not paste with formatting — plain paste only)", False),
        ("", False),
        ("HOW TO EXPORT & PASTE — DOORDASH", True),
        ("1. Log into DoorDash Merchant Portal", False),
        ("2. Go to: Financials > Report Builder", False),
        ("3. Select the week you are reporting (Monday to Sunday)", False),
        ("4. Download CSV", False),
        ("5. Open the CSV, select all, copy", False),
        ("6. Click into cell A3 of the DoorDash-Import tab", False),
        ("7. Paste (plain paste only)", False),
        ("", False),
        ("HOW TO EXPORT & PASTE — UBER EATS", True),
        ("1. Log into Uber Eats Manager", False),
        ("2. Go to: Analytics > Reports", False),
        ("3. Select 'Download Report' and choose the reporting week", False),
        ("4. Open the CSV, select all, copy", False),
        ("5. Click into cell A3 of the UberEats-Import tab", False),
        ("6. Paste (plain paste only)", False),
        ("", False),
        ("HOW TO EXPORT & PASTE — GRUBHUB", True),
        ("1. Log into Grubhub Restaurant Hub", False),
        ("2. Go to: Reports", False),
        ("3. Select the week and click 'Export'", False),
        ("4. Open the CSV, select all, copy", False),
        ("5. Click into cell A3 of the Grubhub-Import tab", False),
        ("6. Paste (plain paste only)", False),
        ("NOTE: Grubhub payouts are sometimes delayed 7–10 days. If the Grubhub column "
         "shows $0 on Monday, that is normal — check back Tuesday or Wednesday and update "
         "the Last Updated cell in the Grubhub-Import tab.", False),
        ("", False),
        ("HOW TO EXPORT & PASTE — BEK ENTREE", True),
        ("1. Log into BEK Entree Portal", False),
        ("2. Go to: Order History > Export Invoice CSV", False),
        ("3. Select date range matching your reporting week", False),
        ("4. Open the CSV, select all, copy", False),
        ("5. Click into cell A3 of the BEK-Import tab", False),
        ("6. Paste (plain paste only)", False),
        ("", False),
        ("TROUBLESHOOTING", True),
        ("If you see $0 or ERROR in the Summary tab, check the validation row (row 2) in "
         "each import tab. A red cell in row 2 means that column did not paste as a number "
         "— the data came in as text. Try pasting again without formatting, or paste into "
         "Notepad first and re-copy to strip formatting.", False),
        ("", False),
        ("If MATCH column errors (#N/A) appear, the column header in the import tab does not "
         "match the header in your CSV export. Update row 1 of the import tab to match the "
         "exact column name in your CSV file.", False),
    ]

    for r, (text, is_header) in enumerate(content, start=2):
        cell = ws.cell(row=r, column=1, value=text)
        if is_header:
            cell.font = FONT_SECTION
            cell.fill = PatternFill("solid", fgColor="E8F0FE")
            ws.row_dimensions[r].height = 20
        else:
            cell.font = FONT_DEFAULT
            cell.fill = FILL_WHITE
            ws.row_dimensions[r].height = 40 if len(text) > 80 else 18
        cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

    freeze(ws, "A2")


# Key: list of column indices (0-based) that should be numeric in each import tab
NUMERIC_COLS = {
    "Square-Import":    {"Net Sales": 3, "Gross Sales": 4},
    "DoorDash-Import":  {"Net Payout": 4, "Order Count": 5},
    "UberEats-Import":  {"Net Payout": 4, "Trips": 5},
    "Grubhub-Import":   {"Net Payout": 5, "Orders": 6},
    "BEK-Import":       {"Total": 6, "Quantity": 4},
}


def build_import_tab(ws, tab_name, headers, sample_rows):
    """Build a platform import tab with headers, validation row, and sample data."""
    apply_tab_color(ws, TAB_IMPORT)

    # --- Row 1: PLACEHOLDER notice as a merged note above headers ---
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(headers))
    notice_cell = ws.cell(row=1, column=1,
        value="PLACEHOLDER HEADERS — Update row 2 to match your actual CSV export column names exactly.")
    notice_cell.font  = Font(name="Calibri", size=10, bold=True, color="7F4F00")
    notice_cell.fill  = PatternFill("solid", fgColor="FFF2CC")
    notice_cell.alignment = ALIGN_CENTER
    ws.row_dimensions[1].height = 20

    # --- Row 2: Column headers ---
    for col_idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=2, column=col_idx)
        style_header_cell(cell, header, fill=FILL_IMPORT_HDR)
        ws.column_dimensions[get_column_letter(col_idx)].width = col_width_for(header)

    freeze(ws, "A3")

    # --- Row 3: Validation row ---
    numeric_map = NUMERIC_COLS.get(tab_name, {})
    # Build a reverse map: header_name -> 1-based col index (based on position in headers list)
    header_col_map = {h: i for i, h in enumerate(headers, start=1)}

    for col_idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=3, column=col_idx)
        col_letter = get_column_letter(col_idx)

        if header in numeric_map or any(h in header for h in ["Net", "Payout", "Total", "Sales", "Count", "Orders", "Trips", "Quantity"]):
            # MATCH-based validation formula referencing row 4 (first data row)
            # Checks: does the value at (first_data_row, this_col) parse as a number?
            formula = (
                f'=IF(ISNUMBER(INDEX({tab_name}!A:Z,4,'
                f'MATCH("{header}",{tab_name}!2:2,0))),"OK",'
                f'"PASTE ERROR - {header} is not a number")'
            )
            cell.value = formula
            cell.fill  = FILL_VALID_BAD
            cell.font  = FONT_VALID_BAD
            cell.alignment = ALIGN_CENTER
        else:
            # Text/date columns — just note expected type
            cell.value = f'[{header} — text/date]'
            cell.fill  = PatternFill("solid", fgColor="F3F3F3")
            cell.font  = Font(name="Calibri", size=9, color="888888", italic=True)
            cell.alignment = ALIGN_CENTER

        ws.row_dimensions[3].height = 22

    # Conditional formatting: if cell = "OK" → green fill
    from openpyxl.formatting.rule import FormulaRule
    ok_fill = PatternFill(start_color="D9EAD3", end_color="D9EAD3", fill_type="solid")
    ok_font = Font(color="006100", bold=True, name="Calibri", size=10)
    # Apply per-cell since row content varies
    for col_idx in range(1, len(headers) + 1):
        col_letter = get_column_letter(col_idx)
        ws.conditional_formatting.add(
            f"{col_letter}3",
            FormulaRule(
                formula=[f'={col_letter}3="OK"'],
                fill=ok_fill,
                font=ok_font,
                stopIfTrue=False,
            )
        )

    # --- Rows 4+: Sample data ---
    for r_idx, row_data in enumerate(sample_rows, start=4):
        for c_idx, value in enumerate(row_data, start=1):
            cell = ws.cell(row=r_idx, column=c_idx, value=value)
            cell.font = FONT_DEFAULT
            cell.alignment = ALIGN_LEFT
            # Alternating row color
            if r_idx % 2 == 0:
                cell.fill = FILL_ALT_ROW
            else:
                cell.fill = FILL_WHITE

    # --- Last Updated marker ---
    last_data_row = 3 + len(sample_rows)
    label_row = last_data_row + 2
    ws.cell(row=label_row, column=1, value="Last Updated:").font = FONT_BOLD
    date_cell = ws.cell(row=label_row, column=2, value="")
    date_cell.number_format = "YYYY-MM-DD"
    date_cell.fill = PatternFill("solid", fgColor="FFF9C4")
    comment = Comment("Enter the date you pasted this data.", "Build Script")
    date_cell.comment = comment


def build_employee_roster(ws):
    """Build the Employee-Roster reference tab."""
    apply_tab_color(ws, TAB_GREEN)

    headers = ["Employee Name", "Square Name", "Location", "Hourly Rate",
               "Hire Date", "Pay Tier", "Notes"]

    # Row 1: headers
    for col_idx, h in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_idx)
        style_header_cell(cell, h, fill=FILL_CALC_HDR)
        ws.column_dimensions[get_column_letter(col_idx)].width = col_width_for(h, 6)

    freeze(ws, "A2")

    # Data validation: Location dropdown
    loc_ids = ",".join(LOCATIONS.keys())
    loc_dv = DataValidation(
        type="list",
        formula1=f'"{loc_ids}"',
        allow_blank=True,
        showErrorMessage=True,
        errorTitle="Invalid Location",
        error=f"Please select one of: {loc_ids}"
    )
    ws.add_data_validation(loc_dv)

    # Populate sample employees
    for r_idx, emp in enumerate(EMPLOYEE_ROSTER, start=2):
        name, sq_name, loc, rate, hire, tier, notes = emp
        row = [name, sq_name, loc, rate, hire, tier, notes]
        for c_idx, val in enumerate(row, start=1):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.font = FONT_DEFAULT
            cell.alignment = ALIGN_LEFT
            if r_idx % 2 == 0:
                cell.fill = FILL_ALT_ROW
            else:
                cell.fill = FILL_WHITE

        # Hourly Rate: currency format
        ws.cell(row=r_idx, column=4).number_format = '"$"#,##0.00'
        # Hire Date: date format
        ws.cell(row=r_idx, column=5).number_format = "YYYY-MM-DD"
        # Location: add to data validation range
        loc_dv.add(ws.cell(row=r_idx, column=3))

    # Note about Square Name column
    note_row = len(EMPLOYEE_ROSTER) + 3
    note_cell = ws.cell(row=note_row, column=1,
        value="NOTE: 'Square Name' must match the employee name exactly as it appears in Square's clock-in export. "
              "This is the VLOOKUP key for labor cost calculations. Nicknames, capitalization, and spacing must match.")
    note_cell.font  = Font(name="Calibri", size=10, italic=True, color="666666")
    note_cell.alignment = Alignment(horizontal="left", wrap_text=True)
    ws.merge_cells(start_row=note_row, start_column=1, end_row=note_row, end_column=7)
    ws.row_dimensions[note_row].height = 40


def build_prior_week(ws):
    """Build the Prior-Week snapshot tab."""
    apply_tab_color(ws, TAB_AMBER)

    headers = PRIOR_WEEK_HEADERS

    # Row 1: headers
    for col_idx, h in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_idx)
        style_header_cell(cell, h, fill=FILL_CALC_HDR)
        ws.column_dimensions[get_column_letter(col_idx)].width = col_width_for(h, 4)
    ws.row_dimensions[1].height = 30

    # Column A = date format
    ws.column_dimensions["A"].width = 16

    freeze(ws, "B2")

    # Row 2: prior week sample data (week ending 2026-03-09)
    for c_idx, val in enumerate(PRIOR_WEEK_SAMPLE, start=1):
        cell = ws.cell(row=2, column=c_idx, value=val)
        cell.font = FONT_DEFAULT
        cell.fill = FILL_ALT_ROW
        cell.alignment = ALIGN_CENTER
        if c_idx == 1:
            cell.number_format = "YYYY-MM-DD"
        elif "%" in headers[c_idx - 1]:
            cell.number_format = "0.0%"
        elif "Net Revenue" in headers[c_idx - 1]:
            cell.number_format = '"$"#,##0.00'

    # Row 3: empty (current week — to be filled from Summary after each Monday paste)
    empty_label = ws.cell(row=3, column=1, value="2026-03-16")
    empty_label.number_format = "YYYY-MM-DD"
    empty_label.font = Font(name="Calibri", size=11, color="AAAAAA", italic=True)
    empty_label.fill = FILL_WHITE
    note = Comment(
        "This row will hold the current week's KPIs after Monday reporting is complete. "
        "Copy values from Summary tab (paste as VALUES only) so next week's WoW formulas can reference them.",
        "Build Script"
    )
    empty_label.comment = note


def build_location_calc(ws, loc_id):
    """Build a Location Calc tab (structure only — formulas added in Plan 02)."""
    apply_tab_color(ws, TAB_CALC)
    full_name = LOCATIONS[loc_id]

    # Row 1: Location name merged across A-F
    ws.merge_cells("A1:F1")
    header_cell = ws["A1"]
    header_cell.value     = full_name
    header_cell.font      = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
    header_cell.fill      = FILL_CALC_HDR
    header_cell.alignment = ALIGN_CENTER
    ws.row_dimensions[1].height = 28

    # Row 2: Week Ending label + blank date cell
    ws.cell(row=2, column=1, value="Week Ending:").font = FONT_BOLD
    ws.cell(row=2, column=1).alignment = ALIGN_LEFT
    date_cell = ws.cell(row=2, column=2, value="")
    date_cell.number_format = "YYYY-MM-DD"
    date_cell.fill = PatternFill("solid", fgColor="FFF9C4")
    date_note = Comment(
        "Link this to the master week-ending date cell, or enter manually each Monday.",
        "Build Script"
    )
    date_cell.comment = date_note

    # Column headers row 3 (blank separator) and then B-E
    ws.cell(row=3, column=2, value="This Week").font  = FONT_BOLD
    ws.cell(row=3, column=3, value="Prior Week").font = FONT_BOLD
    ws.cell(row=3, column=4, value="WoW Change").font = FONT_BOLD
    ws.cell(row=3, column=5, value="WoW %").font      = FONT_BOLD
    for c in [2, 3, 4, 5]:
        cell = ws.cell(row=3, column=c)
        cell.fill      = FILL_CALC_HDR
        cell.font      = FONT_HEADER
        cell.alignment = ALIGN_CENTER

    # Column widths
    ws.column_dimensions["A"].width = 24
    ws.column_dimensions["B"].width = 16
    ws.column_dimensions["C"].width = 16
    ws.column_dimensions["D"].width = 16
    ws.column_dimensions["E"].width = 12

    # --- Section: Revenue Breakdown ---
    ws.cell(row=4, column=1, value="Revenue Breakdown").font = FONT_SECTION
    ws.cell(row=4, column=1).fill = PatternFill("solid", fgColor="E8F0FE")
    ws.merge_cells("A4:E4")

    revenue_labels = [
        "Square Net Sales",
        "DoorDash Net Revenue",
        "UberEats Net Revenue",
        "Grubhub Net Revenue",
        "Total Net Revenue",
    ]
    for i, label in enumerate(revenue_labels, start=5):
        cell = ws.cell(row=i, column=1, value=label)
        cell.font = FONT_BOLD if label.startswith("Total") else FONT_DEFAULT
        cell.alignment = ALIGN_LEFT
        if label.startswith("Total"):
            cell.fill = PatternFill("solid", fgColor="E8F0FE")
            for c in [2, 3, 4, 5]:
                ws.cell(row=i, column=c).fill = PatternFill("solid", fgColor="E8F0FE")
        # Format B and C as currency, E as percentage
        ws.cell(row=i, column=2).number_format = '"$"#,##0.00'
        ws.cell(row=i, column=3).number_format = '"$"#,##0.00'
        ws.cell(row=i, column=4).number_format = '"$"#,##0.00'
        ws.cell(row=i, column=5).number_format = '0.0%'

    # --- Section: Cost Metrics ---
    ws.cell(row=10, column=1, value="Cost Metrics").font = FONT_SECTION
    ws.cell(row=10, column=1).fill = PatternFill("solid", fgColor="E8F0FE")
    ws.merge_cells("A10:E10")

    cost_labels = ["BEK Purchases", "Purchase Cost %"]
    for i, label in enumerate(cost_labels, start=11):
        cell = ws.cell(row=i, column=1, value=label)
        cell.font = FONT_DEFAULT
        cell.alignment = ALIGN_LEFT
        ws.cell(row=i, column=2).number_format = '"$"#,##0.00' if "Purchases" in label else '0.0%'
        ws.cell(row=i, column=3).number_format = '"$"#,##0.00' if "Purchases" in label else '0.0%'
        ws.cell(row=i, column=5).number_format = '0.0%'

    # --- Section: Labor ---
    ws.cell(row=13, column=1, value="Labor").font = FONT_SECTION
    ws.cell(row=13, column=1).fill = PatternFill("solid", fgColor="E8F0FE")
    ws.merge_cells("A13:E13")

    labor_labels = ["Estimated Labor Cost", "Labor Cost %"]
    for i, label in enumerate(labor_labels, start=14):
        cell = ws.cell(row=i, column=1, value=label)
        cell.font = FONT_DEFAULT
        cell.alignment = ALIGN_LEFT
        ws.cell(row=i, column=2).number_format = '"$"#,##0.00' if "Cost $" in label or "Estimated" in label else '0.0%'
        ws.cell(row=i, column=3).number_format = '"$"#,##0.00' if "Estimated" in label else '0.0%'
        ws.cell(row=i, column=5).number_format = '0.0%'

    # --- Section: Volume ---
    ws.cell(row=16, column=1, value="Volume").font = FONT_SECTION
    ws.cell(row=16, column=1).fill = PatternFill("solid", fgColor="E8F0FE")
    ws.merge_cells("A16:E16")

    volume_labels = ["Total Orders", "Avg Ticket Size"]
    for i, label in enumerate(volume_labels, start=17):
        cell = ws.cell(row=i, column=1, value=label)
        cell.font = FONT_DEFAULT
        cell.alignment = ALIGN_LEFT
        if "Avg Ticket" in label:
            ws.cell(row=i, column=2).number_format = '"$"#,##0.00'
            ws.cell(row=i, column=3).number_format = '"$"#,##0.00'
            ws.cell(row=i, column=4).number_format = '"$"#,##0.00'
        ws.cell(row=i, column=5).number_format = '0.0%'

    # Note: formulas added in Plan 02
    note_row = 20
    note_cell = ws.cell(row=note_row, column=1,
        value=f"[{loc_id}] Formulas for This Week values will be added in Plan 02 — "
              "once CSV column names are validated with Rez's actual exports.")
    note_cell.font = Font(name="Calibri", size=10, italic=True, color="AAAAAA")
    note_cell.alignment = Alignment(wrap_text=True, horizontal="left")
    ws.merge_cells(f"A{note_row}:E{note_row}")
    ws.row_dimensions[note_row].height = 40


def build_summary(ws):
    """Build the Summary tab (structure only — formulas in Plan 02)."""
    apply_tab_color(ws, TAB_AMBER)

    # Row 1: Title
    ws.merge_cells("A1:F1")
    title_cell = ws["A1"]
    title_cell.value     = "Weekly Report Summary"
    title_cell.font      = Font(name="Calibri", size=18, bold=True, color="1C3557")
    title_cell.fill      = PatternFill("solid", fgColor="FFF2CC")
    title_cell.alignment = ALIGN_CENTER
    ws.row_dimensions[1].height = 36

    # Row 2: Week Ending
    ws.cell(row=2, column=1, value="Week Ending:").font = FONT_BOLD
    week_cell = ws.cell(row=2, column=2, value="")
    week_cell.number_format = "YYYY-MM-DD"
    week_cell.fill = PatternFill("solid", fgColor="FFF9C4")
    week_note = Comment(
        "Enter the Sunday date of the week you are reporting (e.g., 2026-03-15). "
        "WoW comparison formulas reference this cell.",
        "Build Script"
    )
    week_cell.comment = week_note
    ws.row_dimensions[2].height = 20

    # Row 3: blank separator
    ws.row_dimensions[3].height = 8

    # Row 4: Column headers — blank | MML | MMA | MM3 | TS1 | TS2
    loc_order = ["MML", "MMA", "MM3", "TS1", "TS2"]
    loc_full  = [LOCATIONS[l] for l in loc_order]

    header_labels = [""] + loc_full
    for c_idx, label in enumerate(header_labels, start=1):
        cell = ws.cell(row=4, column=c_idx, value=label)
        cell.font      = FONT_HEADER
        cell.fill      = PatternFill("solid", fgColor="434343")
        cell.alignment = ALIGN_CENTER
    ws.row_dimensions[4].height = 28

    # Brand color bands — apply to rows 5-14 for Moto Medi (cols B-D) and Tikka Shack (cols E-F)
    for row in range(5, 15):
        for col in range(2, 5):  # B-D = MML, MMA, MM3 = Moto Medi
            ws.cell(row=row, column=col).fill = FILL_MOTO_MEDI
        for col in range(5, 7):  # E-F = TS1, TS2 = Tikka Shack
            ws.cell(row=row, column=col).fill = FILL_TIKKA_SHACK

    # KPI rows (rows 5-14)
    kpi_rows = [
        (5,  "Net Revenue",      False),
        (6,  "  WoW",            True),
        (7,  "Purchase Cost %",  False),
        (8,  "  WoW",            True),
        (9,  "Labor Cost %",     False),
        (10, "  WoW",            True),
        (11, "Order Volume",     False),
        (12, "  WoW",            True),
        (13, "Avg Ticket",       False),
        (14, "  WoW",            True),
    ]
    for (row_num, label, is_wow) in kpi_rows:
        cell = ws.cell(row=row_num, column=1, value=label)
        cell.font = Font(name="Calibri", size=11, italic=is_wow,
                         color="666666" if is_wow else "111111",
                         bold=not is_wow)
        cell.alignment = ALIGN_LEFT
        ws.row_dimensions[row_num].height = 20

    # Freeze row 4 and column A
    freeze(ws, "B5")

    # Column widths
    ws.column_dimensions["A"].width = 20
    for col_letter in ["B", "C", "D", "E", "F"]:
        ws.column_dimensions[col_letter].width = 18

    # Print area
    ws.print_area = "A1:F14"

    # Placeholder note
    note_cell = ws.cell(row=16, column=1,
        value="Formulas for all KPI cells will be added in Plan 02, after CSV column names are "
              "confirmed with Rez's real exports. Brand color bands: columns B-D = Moto Medi (orange), "
              "columns E-F = Tikka Shack (teal).")
    note_cell.font = Font(name="Calibri", size=10, italic=True, color="AAAAAA")
    note_cell.alignment = Alignment(wrap_text=True, horizontal="left")
    ws.merge_cells("A16:F16")
    ws.row_dimensions[16].height = 50


# ==============================================================================
# MAIN
# ==============================================================================

def build_workbook():
    print("Building Rez Weekly Report workbook...")

    wb = Workbook()

    # Remove default sheet
    if "Sheet" in wb.sheetnames:
        del wb["Sheet"]

    # Tab definitions: (name, tab_color, builder_func)
    tab_defs = [
        ("Instructions",    TAB_GREEN,  lambda ws: build_instructions(ws)),
        ("Square-Import",   TAB_IMPORT, lambda ws: build_import_tab(ws, "Square-Import",    SQUARE_HEADERS,   SQUARE_SAMPLE_ROWS)),
        ("DoorDash-Import", TAB_IMPORT, lambda ws: build_import_tab(ws, "DoorDash-Import",  DOORDASH_HEADERS, DOORDASH_SAMPLE_ROWS)),
        ("UberEats-Import", TAB_IMPORT, lambda ws: build_import_tab(ws, "UberEats-Import",  UBEREATS_HEADERS, UBEREATS_SAMPLE_ROWS)),
        ("Grubhub-Import",  TAB_IMPORT, lambda ws: build_import_tab(ws, "Grubhub-Import",   GRUBHUB_HEADERS,  GRUBHUB_SAMPLE_ROWS)),
        ("BEK-Import",      TAB_IMPORT, lambda ws: build_import_tab(ws, "BEK-Import",       BEK_HEADERS,      BEK_SAMPLE_ROWS)),
        ("Employee-Roster", TAB_GREEN,  lambda ws: build_employee_roster(ws)),
        ("Prior-Week",      TAB_AMBER,  lambda ws: build_prior_week(ws)),
        ("MML-Calc",        TAB_CALC,   lambda ws: build_location_calc(ws, "MML")),
        ("MMA-Calc",        TAB_CALC,   lambda ws: build_location_calc(ws, "MMA")),
        ("MM3-Calc",        TAB_CALC,   lambda ws: build_location_calc(ws, "MM3")),
        ("TS1-Calc",        TAB_CALC,   lambda ws: build_location_calc(ws, "TS1")),
        ("TS2-Calc",        TAB_CALC,   lambda ws: build_location_calc(ws, "TS2")),
        ("Summary",         TAB_AMBER,  lambda ws: build_summary(ws)),
    ]

    for tab_name, tab_color, builder_fn in tab_defs:
        print(f"  Building tab: {tab_name}...")
        ws = wb.create_sheet(title=tab_name)
        apply_tab_color(ws, tab_color)
        builder_fn(ws)

    print(f"\nSaving workbook to: {OUTPUT_PATH}")
    wb.save(OUTPUT_PATH)
    print(f"Done. File saved: {OUTPUT_PATH}")

    # Quick sanity check
    wb2 = openpyxl.load_workbook(OUTPUT_PATH)
    expected_tabs = [t[0] for t in tab_defs]
    actual_tabs   = wb2.sheetnames
    if actual_tabs != expected_tabs:
        print(f"WARNING: Tab order mismatch.\n  Expected: {expected_tabs}\n  Got:      {actual_tabs}")
    else:
        print(f"Verified: All {len(expected_tabs)} tabs present in correct order.")

    return OUTPUT_PATH


if __name__ == "__main__":
    build_workbook()
