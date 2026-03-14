"""
sample_data.py — Placeholder/sample data for Rez Weekly Report workbook.

IMPORTANT: Column headers below are PLACEHOLDERS based on documented export formats.
Rez must validate actual column names from his real CSV exports before finalizing
any MATCH() formulas in the workbook.

Week of 2026-03-09 to 2026-03-15 used for all sample data.
"""

# ==============================================================================
# PLACEHOLDER COLUMN HEADERS (must validate against Rez's actual CSV exports)
# ==============================================================================

SQUARE_HEADERS = [
    "Date", "Location", "Category", "Net Sales", "Gross Sales",
    "Discounts", "Tax", "Tips", "Refunds"
]

DOORDASH_HEADERS = [
    "Date", "Store Name", "Subtotal", "Commission", "Net Payout",
    "Order Count", "Avg Order Value"
]

UBEREATS_HEADERS = [
    "Date", "Restaurant Name", "Sales", "Marketplace Fee", "Net Payout",
    "Trips", "Avg Basket"
]

GRUBHUB_HEADERS = [
    "Date", "Restaurant", "Food Sales", "Delivery Fee",
    "Grubhub Commission", "Net Payout", "Orders"
]

BEK_HEADERS = [
    "Invoice Date", "Invoice Number", "Item Description",
    "Category", "Quantity", "Unit Price", "Total"
]

SQUARE_LABOR_HEADERS = [
    "Date", "Employee Name", "Location", "Clock In", "Clock Out",
    "Regular Hours", "Overtime Hours", "Total Hours"
]

# ==============================================================================
# LOCATION & BRAND REFERENCE DATA
# ==============================================================================

LOCATIONS = {
    "MML": "Moto Medi Lubbock",
    "MMA": "Moto Medi Amarillo",
    "MM3": "Moto Medi 3rd",
    "TS1": "Tikka Shack 1",
    "TS2": "Tikka Shack 2",
}

BRANDS = {
    "Moto Medi": ["MML", "MMA", "MM3"],
    "Tikka Shack": ["TS1", "TS2"],
}

# ==============================================================================
# SAMPLE DATA ROWS — week of 2026-03-09 to 2026-03-15
# ==============================================================================

# Square Sales Summary sample data
# Columns: Date, Location, Category, Net Sales, Gross Sales, Discounts, Tax, Tips, Refunds
SQUARE_SAMPLE_ROWS = [
    ["2026-03-09", "Moto Medi Lubbock",   "Food & Drink", 1840.00, 1950.00,  55.00, 152.10, 0,  15.00],
    ["2026-03-10", "Moto Medi Lubbock",   "Food & Drink", 2120.50, 2230.00,  42.00, 175.32, 0,  12.50],
    ["2026-03-11", "Moto Medi Lubbock",   "Food & Drink", 2340.00, 2450.00,  60.00, 193.62, 0,  50.00],
    ["2026-03-12", "Moto Medi Lubbock",   "Food & Drink", 2050.75, 2160.00,  55.25, 169.70, 0,  29.25],
    ["2026-03-13", "Moto Medi Lubbock",   "Food & Drink", 2490.00, 2610.00,  70.00, 205.93, 0,  30.00],
    ["2026-03-09", "Moto Medi Amarillo",  "Food & Drink", 1540.00, 1640.00,  45.00, 127.41, 0,  10.00],
    ["2026-03-10", "Moto Medi Amarillo",  "Food & Drink", 1680.25, 1790.00,  60.00, 139.04, 0,  29.75],
    ["2026-03-11", "Moto Medi Amarillo",  "Food & Drink", 1820.00, 1940.00,  65.00, 150.56, 0,  20.00],
    ["2026-03-12", "Moto Medi Amarillo",  "Food & Drink", 1590.50, 1690.00,  50.00, 131.54, 0,  19.50],
    ["2026-03-13", "Moto Medi Amarillo",  "Food & Drink", 1920.00, 2040.00,  70.00, 158.88, 0,  20.00],
    ["2026-03-09", "Moto Medi 3rd",       "Food & Drink", 1240.00, 1320.00,  35.00, 102.59, 0,  10.00],
    ["2026-03-10", "Moto Medi 3rd",       "Food & Drink", 1380.50, 1470.00,  40.00, 114.16, 0,  19.50],
    ["2026-03-11", "Moto Medi 3rd",       "Food & Drink", 1450.00, 1540.00,  42.00, 119.93, 0,  22.00],
    ["2026-03-12", "Moto Medi 3rd",       "Food & Drink", 1310.75, 1400.00,  38.25, 108.39, 0,  20.25],
    ["2026-03-13", "Moto Medi 3rd",       "Food & Drink", 1520.00, 1610.00,  45.00, 125.65, 0,  20.00],
    ["2026-03-09", "Tikka Shack 1",       "Food & Drink", 1090.00, 1160.00,  30.00,  90.19, 0,  10.00],
    ["2026-03-10", "Tikka Shack 1",       "Food & Drink", 1210.50, 1290.00,  35.00, 100.12, 0,  14.50],
    ["2026-03-11", "Tikka Shack 1",       "Food & Drink", 1320.00, 1400.00,  40.00, 109.14, 0,  20.00],
    ["2026-03-12", "Tikka Shack 1",       "Food & Drink", 1150.25, 1230.00,  32.00,  95.09, 0,  17.75],
    ["2026-03-13", "Tikka Shack 1",       "Food & Drink", 1390.00, 1480.00,  42.00, 114.94, 0,  18.00],
    ["2026-03-09", "Tikka Shack 2",       "Food & Drink",  980.00, 1050.00,  28.00,  81.03, 0,  10.00],
    ["2026-03-10", "Tikka Shack 2",       "Food & Drink", 1060.25, 1130.00,  30.00,  87.69, 0,  19.75],
    ["2026-03-11", "Tikka Shack 2",       "Food & Drink", 1180.00, 1260.00,  35.00,  97.58, 0,  15.00],
    ["2026-03-12", "Tikka Shack 2",       "Food & Drink", 1020.50, 1090.00,  29.50,  84.30, 0,  20.00],
    ["2026-03-13", "Tikka Shack 2",       "Food & Drink", 1140.00, 1220.00,  33.00,  94.25, 0,  13.00],
]

# DoorDash sample data
# Columns: Date, Store Name, Subtotal, Commission, Net Payout, Order Count, Avg Order Value
DOORDASH_SAMPLE_ROWS = [
    ["2026-03-09", "Moto Medi Lubbock",  980.00,  196.00,  784.00, 52, 18.85],
    ["2026-03-10", "Moto Medi Lubbock", 1100.00,  220.00,  880.00, 58, 18.97],
    ["2026-03-11", "Moto Medi Lubbock", 1240.00,  248.00,  992.00, 64, 19.38],
    ["2026-03-12", "Moto Medi Lubbock", 1050.00,  210.00,  840.00, 55, 19.09],
    ["2026-03-13", "Moto Medi Lubbock", 1320.00,  264.00, 1056.00, 70, 18.86],
    ["2026-03-09", "Moto Medi Amarillo",  720.00,  144.00,  576.00, 40, 18.00],
    ["2026-03-10", "Moto Medi Amarillo",  810.00,  162.00,  648.00, 44, 18.41],
    ["2026-03-11", "Moto Medi Amarillo",  890.00,  178.00,  712.00, 48, 18.54],
    ["2026-03-12", "Moto Medi Amarillo",  760.00,  152.00,  608.00, 42, 18.10],
    ["2026-03-13", "Moto Medi Amarillo",  940.00,  188.00,  752.00, 52, 18.08],
    ["2026-03-09", "Moto Medi 3rd",       560.00,  112.00,  448.00, 32, 17.50],
    ["2026-03-10", "Moto Medi 3rd",       620.00,  124.00,  496.00, 35, 17.71],
    ["2026-03-11", "Moto Medi 3rd",       710.00,  142.00,  568.00, 40, 17.75],
    ["2026-03-12", "Moto Medi 3rd",       590.00,  118.00,  472.00, 34, 17.35],
    ["2026-03-13", "Moto Medi 3rd",       680.00,  136.00,  544.00, 38, 17.89],
    ["2026-03-09", "Tikka Shack 1",       490.00,   98.00,  392.00, 28, 17.50],
    ["2026-03-10", "Tikka Shack 1",       540.00,  108.00,  432.00, 31, 17.42],
    ["2026-03-11", "Tikka Shack 1",       610.00,  122.00,  488.00, 35, 17.43],
    ["2026-03-12", "Tikka Shack 1",       510.00,  102.00,  408.00, 29, 17.59],
    ["2026-03-13", "Tikka Shack 1",       660.00,  132.00,  528.00, 38, 17.37],
    ["2026-03-09", "Tikka Shack 2",       410.00,   82.00,  328.00, 24, 17.08],
    ["2026-03-10", "Tikka Shack 2",       450.00,   90.00,  360.00, 26, 17.31],
    ["2026-03-11", "Tikka Shack 2",       520.00,  104.00,  416.00, 30, 17.33],
    ["2026-03-12", "Tikka Shack 2",       430.00,   86.00,  344.00, 25, 17.20],
    ["2026-03-13", "Tikka Shack 2",       570.00,  114.00,  456.00, 33, 17.27],
]

# UberEats sample data
# Columns: Date, Restaurant Name, Sales, Marketplace Fee, Net Payout, Trips, Avg Basket
UBEREATS_SAMPLE_ROWS = [
    ["2026-03-09", "Moto Medi Lubbock",   740.00, 185.00, 555.00, 40, 18.50],
    ["2026-03-10", "Moto Medi Lubbock",   820.00, 205.00, 615.00, 44, 18.64],
    ["2026-03-11", "Moto Medi Lubbock",   940.00, 235.00, 705.00, 50, 18.80],
    ["2026-03-12", "Moto Medi Lubbock",   780.00, 195.00, 585.00, 42, 18.57],
    ["2026-03-13", "Moto Medi Lubbock",   980.00, 245.00, 735.00, 53, 18.49],
    ["2026-03-09", "Moto Medi Amarillo",  560.00, 140.00, 420.00, 30, 18.67],
    ["2026-03-10", "Moto Medi Amarillo",  610.00, 152.50, 457.50, 33, 18.48],
    ["2026-03-11", "Moto Medi Amarillo",  680.00, 170.00, 510.00, 37, 18.38],
    ["2026-03-12", "Moto Medi Amarillo",  590.00, 147.50, 442.50, 32, 18.44],
    ["2026-03-13", "Moto Medi Amarillo",  720.00, 180.00, 540.00, 39, 18.46],
    ["2026-03-09", "Moto Medi 3rd",       420.00, 105.00, 315.00, 23, 18.26],
    ["2026-03-10", "Moto Medi 3rd",       470.00, 117.50, 352.50, 25, 18.80],
    ["2026-03-11", "Moto Medi 3rd",       540.00, 135.00, 405.00, 29, 18.62],
    ["2026-03-12", "Moto Medi 3rd",       440.00, 110.00, 330.00, 24, 18.33],
    ["2026-03-13", "Moto Medi 3rd",       510.00, 127.50, 382.50, 28, 18.21],
    ["2026-03-09", "Tikka Shack 1",       360.00,  90.00, 270.00, 20, 18.00],
    ["2026-03-10", "Tikka Shack 1",       400.00, 100.00, 300.00, 22, 18.18],
    ["2026-03-11", "Tikka Shack 1",       460.00, 115.00, 345.00, 25, 18.40],
    ["2026-03-12", "Tikka Shack 1",       380.00,  95.00, 285.00, 21, 18.10],
    ["2026-03-13", "Tikka Shack 1",       490.00, 122.50, 367.50, 27, 18.15],
    ["2026-03-09", "Tikka Shack 2",       300.00,  75.00, 225.00, 17, 17.65],
    ["2026-03-10", "Tikka Shack 2",       340.00,  85.00, 255.00, 19, 17.89],
    ["2026-03-11", "Tikka Shack 2",       390.00,  97.50, 292.50, 22, 17.73],
    ["2026-03-12", "Tikka Shack 2",       310.00,  77.50, 232.50, 18, 17.22],
    ["2026-03-13", "Tikka Shack 2",       420.00, 105.00, 315.00, 24, 17.50],
]

# Grubhub sample data
# Columns: Date, Restaurant, Food Sales, Delivery Fee, Grubhub Commission, Net Payout, Orders
GRUBHUB_SAMPLE_ROWS = [
    ["2026-03-09", "Moto Medi Lubbock",  380.00, 45.00, 76.00,  259.00, 21],
    ["2026-03-10", "Moto Medi Lubbock",  420.00, 50.00, 84.00,  286.00, 23],
    ["2026-03-11", "Moto Medi Lubbock",  500.00, 58.00, 100.00, 342.00, 27],
    ["2026-03-12", "Moto Medi Lubbock",  410.00, 48.00, 82.00,  280.00, 22],
    ["2026-03-13", "Moto Medi Lubbock",  540.00, 62.00, 108.00, 370.00, 29],
    ["2026-03-09", "Moto Medi Amarillo",  280.00, 34.00, 56.00, 190.00, 16],
    ["2026-03-10", "Moto Medi Amarillo",  320.00, 38.00, 64.00, 218.00, 18],
    ["2026-03-11", "Moto Medi Amarillo",  370.00, 44.00, 74.00, 252.00, 20],
    ["2026-03-12", "Moto Medi Amarillo",  290.00, 35.00, 58.00, 197.00, 16],
    ["2026-03-13", "Moto Medi Amarillo",  400.00, 47.00, 80.00, 273.00, 22],
    ["2026-03-09", "Moto Medi 3rd",       200.00, 25.00, 40.00, 135.00, 11],
    ["2026-03-10", "Moto Medi 3rd",       230.00, 28.00, 46.00, 156.00, 13],
    ["2026-03-11", "Moto Medi 3rd",       270.00, 32.00, 54.00, 184.00, 15],
    ["2026-03-12", "Moto Medi 3rd",       210.00, 26.00, 42.00, 142.00, 12],
    ["2026-03-13", "Moto Medi 3rd",       250.00, 30.00, 50.00, 170.00, 14],
    ["2026-03-09", "Tikka Shack 1",       170.00, 21.00, 34.00, 115.00,  9],
    ["2026-03-10", "Tikka Shack 1",       190.00, 23.00, 38.00, 129.00, 11],
    ["2026-03-11", "Tikka Shack 1",       220.00, 27.00, 44.00, 149.00, 12],
    ["2026-03-12", "Tikka Shack 1",       180.00, 22.00, 36.00, 122.00, 10],
    ["2026-03-13", "Tikka Shack 1",       240.00, 29.00, 48.00, 163.00, 13],
    ["2026-03-09", "Tikka Shack 2",       140.00, 18.00, 28.00,  94.00,  8],
    ["2026-03-10", "Tikka Shack 2",       160.00, 20.00, 32.00, 108.00,  9],
    ["2026-03-11", "Tikka Shack 2",       190.00, 23.00, 38.00, 129.00, 11],
    ["2026-03-12", "Tikka Shack 2",       145.00, 18.00, 29.00,  98.00,  8],
    ["2026-03-13", "Tikka Shack 2",       200.00, 24.00, 40.00, 136.00, 11],
]

# BEK Entree invoice sample data
# Columns: Invoice Date, Invoice Number, Item Description, Category, Quantity, Unit Price, Total
BEK_SAMPLE_ROWS = [
    ["2026-03-10", "INV-2026-0901", "Chicken Thighs 40lb Case",    "Food",     2, 89.50,   179.00],
    ["2026-03-10", "INV-2026-0901", "Jasmine Rice 50lb Bag",       "Food",     3, 42.00,   126.00],
    ["2026-03-10", "INV-2026-0901", "Canola Oil 35lb Jug",         "Food",     4, 38.75,   155.00],
    ["2026-03-10", "INV-2026-0901", "To-Go Containers 200ct",      "Supplies", 5, 18.50,    92.50],
    ["2026-03-10", "INV-2026-0901", "Napkins 4000ct",              "Supplies", 2, 22.00,    44.00],
    ["2026-03-10", "INV-2026-0902", "Ground Beef 80/20 40lb",      "Food",     3, 92.00,   276.00],
    ["2026-03-10", "INV-2026-0902", "Paneer 10lb",                 "Food",     4, 28.50,   114.00],
    ["2026-03-10", "INV-2026-0902", "Spice Blend — Tikka Masala",  "Food",     6, 14.00,    84.00],
    ["2026-03-10", "INV-2026-0902", "Gloves Medium 100ct Box",     "Supplies", 8, 9.75,     78.00],
    ["2026-03-10", "INV-2026-0902", "Cleaning Supplies Bundle",    "Supplies", 3, 31.00,    93.00],
    ["2026-03-13", "INV-2026-0944", "Chicken Thighs 40lb Case",    "Food",     3, 89.50,   268.50],
    ["2026-03-13", "INV-2026-0944", "Flatbread Dough 12pk",        "Food",     6, 19.00,   114.00],
    ["2026-03-13", "INV-2026-0944", "Lentils 25lb Bag",            "Food",     2, 31.00,    62.00],
    ["2026-03-13", "INV-2026-0944", "Sauces — Proprietary Blend",  "Food",     4, 24.00,    96.00],
    ["2026-03-13", "INV-2026-0944", "Kraft Paper Roll 300ft",      "Supplies", 2, 27.50,    55.00],
]

# Square Labor (clock-in/clock-out) sample data
# Columns: Date, Employee Name, Location, Clock In, Clock Out, Regular Hours, Overtime Hours, Total Hours
SQUARE_LABOR_SAMPLE_ROWS = [
    ["2026-03-09", "Marcus Johnson",    "Moto Medi Lubbock",   "08:00", "16:00", 8.0, 0.0, 8.0],
    ["2026-03-09", "Ashley Torres",     "Moto Medi Lubbock",   "10:00", "18:00", 8.0, 0.0, 8.0],
    ["2026-03-09", "Robert Kim",        "Moto Medi Amarillo",  "09:00", "17:00", 8.0, 0.0, 8.0],
    ["2026-03-09", "Destiny Williams",  "Moto Medi Amarillo",  "11:00", "19:00", 8.0, 0.0, 8.0],
    ["2026-03-09", "Jake Hernandez",    "Moto Medi 3rd",       "08:00", "16:00", 8.0, 0.0, 8.0],
    ["2026-03-09", "Priya Patel",       "Tikka Shack 1",       "09:00", "17:00", 8.0, 0.0, 8.0],
    ["2026-03-09", "Carlos Rivera",     "Tikka Shack 1",       "12:00", "20:00", 8.0, 0.0, 8.0],
    ["2026-03-09", "Keisha Brown",      "Tikka Shack 2",       "10:00", "18:00", 8.0, 0.0, 8.0],
    ["2026-03-10", "Marcus Johnson",    "Moto Medi Lubbock",   "08:00", "16:30", 8.0, 0.5, 8.5],
    ["2026-03-10", "Ashley Torres",     "Moto Medi Lubbock",   "10:00", "18:00", 8.0, 0.0, 8.0],
    ["2026-03-10", "Robert Kim",        "Moto Medi Amarillo",  "09:00", "17:00", 8.0, 0.0, 8.0],
    ["2026-03-10", "Jake Hernandez",    "Moto Medi 3rd",       "08:00", "16:00", 8.0, 0.0, 8.0],
    ["2026-03-10", "Priya Patel",       "Tikka Shack 1",       "09:00", "17:30", 8.0, 0.5, 8.5],
    ["2026-03-10", "Keisha Brown",      "Tikka Shack 2",       "10:00", "18:00", 8.0, 0.0, 8.0],
]

# ==============================================================================
# SAMPLE EMPLOYEE ROSTER
# ==============================================================================

# Columns: Employee Name, Square Name (VLOOKUP key), Location, Hourly Rate, Hire Date, Pay Tier, Notes
EMPLOYEE_ROSTER = [
    ["Marcus Johnson",   "Marcus Johnson",   "MML", 16.50, "2024-06-01", "Line Cook",    "Lead cook — Lubbock"],
    ["Ashley Torres",    "Ashley Torres",    "MML", 14.00, "2024-09-15", "Cashier",      "Cross-trained on prep"],
    ["Destiny Williams", "Destiny Williams", "MMA", 14.50, "2025-01-10", "Cashier",      ""],
    ["Robert Kim",       "Robert Kim",       "MMA", 15.75, "2024-08-20", "Line Cook",    ""],
    ["Jake Hernandez",   "Jake Hernandez",   "MM3", 15.00, "2025-03-01", "Line Cook",    "Newer location"],
    ["Priya Patel",      "Priya Patel",      "TS1", 16.00, "2024-07-14", "Line Cook",    "Tikka Shack specialist"],
    ["Carlos Rivera",    "Carlos Rivera",    "TS1", 13.50, "2025-02-01", "Cashier",      ""],
    ["Keisha Brown",     "Keisha Brown",     "TS2", 14.25, "2024-11-05", "Line Cook",    ""],
    ["Devon Scott",      "Devon Scott",      "MML", 12.50, "2025-10-20", "Kitchen Help", "Part-time"],
    ["Jasmine Lee",      "Jasmine Lee",      "TS2", 13.00, "2025-11-01", "Cashier",      "Part-time"],
]

# ==============================================================================
# PRIOR WEEK SNAPSHOT (week ending 2026-03-09)
# ==============================================================================
# Structure matches the Prior-Week tab columns:
# Week Ending | MML Net Rev | MML Purchase% | MML Labor% | MML Orders | MML Avg Ticket
#             | MMA ...     | MM3 ...        | TS1 ...    | TS2 ...

PRIOR_WEEK_HEADERS = [
    "Week Ending",
    "MML Net Revenue", "MML Purchase Cost %", "MML Labor Cost %", "MML Orders", "MML Avg Ticket",
    "MMA Net Revenue", "MMA Purchase Cost %", "MMA Labor Cost %", "MMA Orders", "MMA Avg Ticket",
    "MM3 Net Revenue", "MM3 Purchase Cost %", "MM3 Labor Cost %", "MM3 Orders", "MM3 Avg Ticket",
    "TS1 Net Revenue", "TS1 Purchase Cost %", "TS1 Labor Cost %", "TS1 Orders", "TS1 Avg Ticket",
    "TS2 Net Revenue", "TS2 Purchase Cost %", "TS2 Labor Cost %", "TS2 Orders", "TS2 Avg Ticket",
]

PRIOR_WEEK_SAMPLE = [
    "2026-03-09",
    12050.00, 0.284, 0.312, 387, 19.10,   # MML
    9820.00,  0.301, 0.298, 321, 18.85,   # MMA
    7640.00,  0.318, 0.305, 258, 18.92,   # MM3
    6510.00,  0.312, 0.321, 215, 18.65,   # TS1
    5890.00,  0.296, 0.334, 182, 18.88,   # TS2
]
