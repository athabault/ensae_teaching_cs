#-*- coding: utf-8 -*-
"""
@file
@brief An example of a custom magic for IPython.
"""
import sys

from IPython.core.magic import Magics, magics_class, line_magic, cell_magic
from IPython.core.magic import line_cell_magic
from IPython.core.display import HTML                                

@magics_class
class CustomMagics(Magics):

    @line_magic
    def ENSAEl(self, line):
        """
        This command can be activated by typing::
        
            %ENSAEl
            
        """
        if "site" in line:
            return HTML('<a href="http://www.xavierdupre.fr/app/ensae_teaching_cs/helpsphinx/index.html">ENSAE TD</a>')
        elif "blog" in line :
            return HTML('<a href="http://www.xavierdupre.fr/blog/xd_blog_nojs.html">blog</a>')
        else: 
            raise Exception("unknown command: " + line)
        
        #print("Full access to the main IPython object:", self.shell)
        #print("Variables in the user namespace:", list(self.shell.user_ns.keys()))

    @cell_magic
    def ENSAEb(self, line, cell):
        """
        This command can be activated by typing::
        
            %%ENSAEb
            
        """
        return line, cell

    @line_cell_magic
    def ENSAE(self, line, cell=None):
        """
        This command can be activated by typing::
        
            %ENSAE
            
        Or::
            
            %%ENSAE
            
        """
        if cell is None:
            line = line.strip()
            if line.startswith("download"):
                spl = line.split()
                if len(spl)==2:
                    import pyensae
                    r = pyensae.download_data(spl[1])
                    return r
                else :
                    raise Exception("unable to interpret: " + line)
            else :
                return self.ENSAEl(line)
        else:
            raise Exception("unable to interpret:\n" + cell)
    
    @cell_magic
    def SPEAK(self, line, cell):
        """
        If the OS is Windows, the magic command will tell the text.
        
        The function defines ``%%SPEAK``.
        
        """
        if not sys.platform.startswith("win"):
            raise Exception("Works only on Windows.")
        
        from ..pythonnet import vocal_synthesis
        if line is not None:
            spl = line.strip().split(" ")
            lang = spl[0]
            filename = " ".join(spl[1:]) if len(spl) > 1 else ""
            
        if lang == "-h": 
            print(  "Usage: "
                    "   %%SPEAK fr-FR [filename]"
                    "   speech")
        else :
            vocal_synthesis(cell, lang, filename)
            
    @cell_magic
    def CS(self, line, cell):
        """
        Defines command ``%%CS``.
        """
        if not sys.platform.startswith("win"):
            raise Exception("Works only on Windows.")
        
        from ..tips_tricks.pythoncs import create_cs_function
        if line is not None:
            spl = line.strip().split(" ")
            name = spl[0]
            deps = " ".join(spl[1:]) if len(spl) > 1 else ""
            deps = deps.split(";")
            
        if name == "-h": 
            print(  "Usage: "
                    "   %%CS function_name dependency1;dependency2"
                    "   function code")
        else :
            try:
                f = create_cs_function(name, cell, deps)
            except Exception as e :
                print(e)
                return 
            if self.shell is not None:
                self.shell.user_ns[name] = f
            return f

def register_magics():
    """
    register magics function, can be called from a notebook
    """
    ip = get_ipython()
    ip.register_magics(CustomMagics)
    