import os
import shutil
import zipfile

class ZipHanding:
    """Decompress the ZIP file or compress the file into a ZIP file"""
    def unzip(self, zip_path, dp=None):  
        """
        Unzip zip file to a folder
        
        Parameters
        ---------
        zip_path: Zip file path 
        dp: Decompression path

        Returns
        ---------
        dir_path: The path of the extracted folder

        Raises
        ---------
        """
        if dp == None:
            ## By default, it is decompressed to the current directory
            dp = zip_path.rsplit('.', 1)[0]
        if os.path.exists(dp):
            shutil.rmtree(dp)        
        with zipfile.ZipFile(zip_path, 'r') as f:
            for fn in f.namelist():
                f.extract(fn, dp)
        return dp

    def __rm_file_folder(self, fp):
        '''
        remove file or folder
        '''
        if os.path.exists(fp) and os.path.isfile(fp):
            os.remove(fp)
        elif os.path.exists(fp) and os.path.isdir(fp):
            shutil.rmtree(fp)
        else:
            raise FileNotFoundError('File not found')

    def __rename_correctly(self, string):
        '''
        Rename the garbled characters extracted from the window package
        '''
        try:
            new_string = string.encode('cp437').decode('utf-8')
        except:
            try:
                new_string = string.encode('cp437').decode('gbk')
            except:
                new_string = string.encode('utf-8').decode('utf-8')
        return  new_string
        
    def __rm_special_name_folder(self, dir_path, folder_name='__MACOSX'): 
        '''
        Delete the folder named 'xxxx' if it exists.
        The default folder name is __MACOSX.
        '''
        for root, dirs, files in os.walk(dir_path, topdown=False):
            for name in dirs:
                if name == folder_name :
                    shutil.rmtree(os.path.join(root, name))  

    def __standard_zip_dir(self, dir_path):
        for root, dirs, filenames in os.walk(dir_path):
            for fn in filenames:
                fp = os.path.join(root, fn)
                new_fp = os.path.join(dir_path, self.__rename_correctly(fn))
                os.rename(fp, new_fp)
                
        for root, dirs, filenames in os.walk(dir_path):
            for folder in dirs:
                dp = os.path.join(root, folder)
                self.__rm_file_folder(dp)
                self.__rm_special_name_folder(dir_path)   
                 
    @classmethod
    def decompression(cls, zip_path):
        dir_path = cls().unzip(zip_path)
        cls().__standard_zip_dir(dir_path)      
        return dir_path

    @classmethod
    def zip_file(cls, dfp, out_path=None):
        """
        Compresses the specified folder

        Parameters
        ---------
        dfp: Destination folder or file path.
        out_path: Save path of the compressed file +xxxx.zip.

        Returns
        ---------
        """

        if os.path.isdir(dfp):   
            if out_path == None:
                out_path = dfp + '.zip'
            with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as f:
                    for root, _, filenames in os.walk(dfp):
                        for fn in filenames:
                            f.write(filename=os.path.join(root, fn), arcname=fn)
        else:
            if out_path == None:
                out_path = dfp.rsplit('.', 1)[0] + '.zip'
            with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as f:
                f.write(dfp, dfp.rsplit('/', 1)[1])
        print(out_path)

if __name__=='__main__':

    zip_path = 'app/data/input/三元组数据集_云测早期标注.zip'
    dir_path = ZipHanding.decompression(zip_path)
    print(f'decompression path is  {dir_path}')
    res = dfp = 'app/data/input/三元组数据集_云测早期标注'
    print(f'zip_file path is {res}')