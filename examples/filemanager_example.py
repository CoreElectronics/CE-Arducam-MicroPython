
import uos
import ujson


class FileManager:
    def __init__(self, file_manager_name='filemanager.log'):
        
        self.FILE_MANAGER_LOG_NAME = file_manager_name
        self.last_request_filename = None
        self.suffix = None
        count = 0
        file_dict = {}
        # Ensure file is present
        if self.FILE_MANAGER_LOG_NAME not in uos.listdir():
            with open(self.FILE_MANAGER_LOG_NAME, 'w') as f:
                f.write(ujson.dumps(file_dict))
            
        # Check if the filename already exists in the storage
        with open(self.FILE_MANAGER_LOG_NAME, 'r') as f:
            self.file_dict = ujson.loads(f.read())


    def new_jpg_fn(self, requested_filename=None):
        return (self.new_filename(requested_filename) + '.jpg')
    
#     def new_fn_custom(self, suffix, requested_filename=None, suffix):
#         return (self.new_filename(requested_filename) + suffix)
        
    def new_filename(self, requested_filename):
        count = 0
        self.last_request_filename = requested_filename
        
        if requested_filename == None and self.last_request_filename == None:
            raise Exception('Please enter a filename for the first use of the function')
        
        if requested_filename in self.file_dict:
            count = self.file_dict[requested_filename] + 1
        self.file_dict[requested_filename] = count
        
        self.save_manager_file()
        new_filename = f"{requested_filename}_{count}" if count > 0 else f"{requested_filename}"
        
        return new_filename
    
    def save_manager_file(self):
        # Save the updated list back to the storage
        with open(self.FILE_MANAGER_LOG_NAME, 'w') as f:
            f.write(ujson.dumps(self.file_dict))




################################################################## CODE ACTUAL ##################################################################



fm = FileManager()
print(fm.new_jpg_filename('image'))
