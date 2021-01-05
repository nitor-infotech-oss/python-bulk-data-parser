"""
This file contains all the configuration required for validation to process excel/csv data
Like Columns expected, Required columns, Boolean columns
"""

SUPPORTED_FILE_TYPES = ['.csv', '.xls', '.xlsx']
BOOLEAN_FIELD_VALUES = ['on', 'off']

# Messages
MISSING_REQUIRED_COLUMN = "Missing required fields mapping"
MISSING_REQUIRED_COLUMN_VALUE = ""
INVALID_BOOLEAN_FIELD = "Invalid value in column's {}. It must contain string 'on' or 'off'"
MISSING_FIELD_MAPPINGS = 'Missing database fields mapping'
SUCCESSFULLY_UPLOADED = 'Successfully Uploaded'
ERROR_IN_UPLOAD = 'ERROR'
