from logging import Formatter


class FileCheck:
    """
    Document Type Checking

    Args:
    fileType: A string or list of strings with a file type suffix.
    """    
    def __init__(self, fileType):
        self.ALLOWED_EXTENSIONS = fileType
        
    def allowed_file(self, fn):
        """
        Args:
            fileType(:obj:'list, str'):
                A string or list of strings with a file type suffix.
        Return:
            :obj:'bool, str'
            file type or False

        Examples
        ----------
        Check if the file is DOCX
        >>>docxChick = FileCheck(['docx'])
        >>>docxChick.allowed_file('abcd.docx')
        >>>'docx'
        """
        if '.' in fn and fn.rsplit('.', 1)[1] in self.ALLOWED_EXTENSIONS:
            return True
        else:
            return False

if __name__=='__main__':

    docx_chick = FileCheck(['docx'])
    result = docx_chick.allowed_file('abcd.docx')
    print(result)