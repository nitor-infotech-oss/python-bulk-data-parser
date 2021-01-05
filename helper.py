import os
import json
import _thread
import pandas as pd
import config as upload_config

class Data_Parser:
    entity_type = None
    sheet_name = None
    
    def __init__(self, uploaded_file, entity_type):
        self.entity_type = entity_type
        self.df = None
        self.file_data = []
        self.entity_config_data = {}
        self.required_fields = {}
        self.boolean_fields = {}
        self.uploaded_file = uploaded_file
        self.file_ext = os.path.splitext(self.uploaded_file)[1]
        self.get_entity_config()
        self.validate_file_type()
        self.get_file_data()
        self.get_file_headers()
        self.update_headers_with_db_field_names()
        self.check_required_column_in_headers()

    def get_entity_config(self):
        entity_config_file = 'Config-Files/{}.json'.format(self.entity_type)
        with open(entity_config_file) as f:
            self.entity_config_data = json.load(f)
        
        # create required fields mapping
        for req in self.entity_config_data['required']:
            self.required_fields[req] = self.entity_config_data['fields'][req]
        
        # create boolean fields mapping
        for bool_field in self.entity_config_data['boolean']:
            self.boolean_fields[bool_field] = self.entity_config_data['fields'][bool_field]
        
        
    def validate_file_type(self):
        # check file type CSV/Excel
        if self.file_ext not in upload_config.SUPPORTED_FILE_TYPES:
            raise TypeError("Invalid File Type")
            
    def get_sheet_names(self):
        xl = pd.ExcelFile(self.uploaded_file)
        all_sheets = xl.sheet_names
        return all_sheets

    def get_file_data(self):
        # check file type CSV/Excel
        if self.file_ext == ".csv":
            # Read CSV data & replaved nan to blank ''
            file_data = pd.read_csv(self.uploaded_file).fillna('')
            file_data.drop(file_data.columns[file_data.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
        elif self.file_ext in [".xls",".xlsx"]:
            # get all available sheets in the uploaded file
            excel_sheets = self.get_sheet_names()
            # read data from all sheets
            for excel_sheet in excel_sheets:
                file_data = []
                # Read excel data & replaced nan to blank ''
                self.df = pd.read_excel(self.uploaded_file, sheet_name=excel_sheet).fillna('')
        self.file_data = self.df
    
    def get_file_headers(self):
        self.headers = list(self.file_data.columns.values)

    def get_column_name_mapping_with_fields(self):
        mapping = None
        try:
            mapping = self.entity_config_data['fields']
        except:    
            raise ValueError(upload_config.MISSING_FIELD_MAPPINGS)  

        return mapping

    def check_required_column_in_headers(self):
        # check required fields
        required_columns = self.required_fields.keys()
        header_set = set(self.headers)
        # print("updated headers in validate headers : ",self.updated_headers)
        required_set= set(required_columns)
        
        is_subset = required_set.issubset(header_set)
        if not is_subset :
            # find missing required headers
            missing_headers = list(set(required_set).difference(self.headers))
            error = "Missing required columns : {}".format(', '.join(missing_headers))
            raise ValueError(error)

    def validate_required_column_data(self, row_data):
        required_columns = self.required_fields
        missing_columns = []
        
        status = True
        # check is required column value available or not
        for field in required_columns:
            column = required_columns[field]
            col_data = row_data[column]
            if str(col_data).strip() == '':
                status = False
                missing_columns.append(field)

        return status, missing_columns

    def validate_boolean_fields(self, row_data):
        valid_boolean_values = upload_config.BOOLEAN_FIELD_VALUES
        invalid_boolean_fields = []
        status = True
        for field in self.boolean_fields:
            column = self.boolean_fields[field]
            val = row_data[column].lower()
            if column in row_data and val not in valid_boolean_values:
                invalid_boolean_fields.append(field)

        if len(invalid_boolean_fields) > 0:
            status = False        

        return status, invalid_boolean_fields

    def update_headers_with_db_field_names(self):
        db_fields = self.get_column_name_mapping_with_fields()
        updated_headers = [db_fields[header] for header in self.headers]
        self.updated_headers = updated_headers
        self.file_data.columns = updated_headers
        self.file_data = self.file_data.to_dict('record')