import sys, getopt
from helper import Data_Parser
import pandas as pd
import time
from threading import Thread

def main(argv):
    """
    The purpose of this command is to bulk upload profiles.

    An expected entity role must be specified by the user, and if the role doesn't provided 
    then the the operation will be aborted.    
  
    """
    # # Parse the options
    inputfile = ''
    entitytype = ''
    noofthreads = 5

    try:
      opts, args = getopt.getopt(argv,"hi:e:t:",["ifile=","type=","threads="])
    except getopt.GetoptError:
      print('data_parser.py -i <inputfile> -e <entitytype> -t <noofthreads>')
      sys.exit(2)

    options = dict(opts)
    if '-h' in options or not options:
        # Todo - Add one liner explnation for options 
         print('data_parser.py -i <inputfile> -e <entitytype> -t <noofthreads>')
         sys.exit()

    if '-e' in options or '--type' in options:
        entitytype = str(options['-e']) if '-e' in options else str(options['--type']) 
    else:
        raise ValueError('An expected entity type must be specified with --type!')

    if '-i' in options or '--ifile' in options:
        inputfile = str(options['-i']) if '-i' in options else str(options['--ifile']) 
    else:
        raise ValueError('An expected input file must be specified with --ifile!')

    if '-t' in options or '--threads' in options:
        noofthreads = int(options['-t']) if '-t' in options else int(options['--threads']) 
    
    
    helper = Data_Parser(inputfile, entitytype)
    
    # loop over rows to upload data
    file_data = helper.file_data
    n1 = len(file_data)//noofthreads 
    data_chunks = [file_data[i:i+n1] for i in range(0, len(file_data), n1)]
    
    # create a thread list (you'll need it later)
    threads = [Thread(target=process_data, args=(helper, lst, 'tname-{}'.format(i))) for i, lst in enumerate(data_chunks)]
    # start all the threads
    [t.start() for t in threads] 

    # wait for threads to finish
    [t.join() for t in threads]

    # download error data file
    download_error_data(helper, file_data)

    
def process_data(helper, file_data, tname):
    #print("\n\n")
    for row in file_data:
        errors = []
        # check required columns
        is_validated, missing_columns = helper.validate_required_column_data(row)
        if not is_validated:
            err_msg = "Missing required columns data : {}".format(', '.join(missing_columns))
            errors.append(err_msg)
           
        # check valid boolean fields data
        is_boolean_fields_valid, boolean_fields = helper.validate_boolean_fields(row)
        if not is_boolean_fields_valid:
            err_msg = "Invalid data in columns {}. It must contain string 'on' or 'off'.".format(', '.join(boolean_fields))
            errors.append(err_msg)
            
        if errors:
            row['Errors'] = ', '.join(errors)
        else:
            # Here you can perform actual logic if you want to upload data one by one 
            # otherwise you can use parsed data after loop for processing
            row['Success'] = "Successfully passed data validation for this row."

            

def download_error_data(helper, data):
    # Create a Pandas dataframe from the data.
    df = pd.DataFrame(data)

    if helper.file_ext == '.csv':
        file_name = helper.entity_type+'.csv'
        df.to_csv (file_name, index = False, header=True)
    else:
        file_name = helper.entity_type+'.xlsx'
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        df.to_excel(writer, sheet_name=helper.entity_type, index=False)
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
    
if __name__ == "__main__":
   main(sys.argv[1:])