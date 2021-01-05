## Bulk Excel/CSV Data Parser

A Component for reading excel files data and used similar data for bulk data upload after perform validation. Extremely fast, flexible, and easy to use. 

Using the result of this parser you can perform insert/update as per your database structure.

This component is based on the Python Pandas Library. We use Pandas ExcelReader & CSVReader for reading excel & csv respectively.

### Installation

#### Prerequisite:
- Python3


Use the following command to download pip directly,

```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```
Now execute the downloaded file using below command

```bash
python3 get-pip.py
```

```bash
pip3 install pandas
pip3 install xlrd
pip3 install xlsxwriter
```
### Documentation

We have given below functionality here

#### Supported EXCEL & CSV File Format

1. Read Excel/CSV file data
2. Config file validation
3. Data Validations
    - Added file type validation
	- Added required column validation on header
	- Added validation for each row for required data
    - Added Boolean Fields validation
4. Downloads Excel/CSV for status of data.
	- Here we will export excel which will have uploaded data status.
	- Added Errors column if any data for in the row
5. Supports multi threading for data processing

#### Configurations:
- Config file contains all the configuration needed to perform validations on the data. so if you want to add your own entity validations then you have to create new config file similar to user.json in Config-Files folder. 
- config.py contains basic configurations like supported files type, validation messages, etc.
- You can refer files from Sample-Data-Files folder for initial run. 

#### To Run 

```bash
python3 data_parser.py -i <inputfile> -e <entitytype>
```

### Upcoming fetures

1. Validations on date, time fields
2. Google sheet support 