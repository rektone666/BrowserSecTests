# BrowserSecTests
BrowserSecTests is just a small python experiment tool for lazy people like me which automatically execute a series of security test of your browser .
those test are focused to check how and what data can or cannot be retrived from our browser by simply visiting a page . 
it goes through 75 differts test , from VBScript, COOKIES and so on ... 
the code works around BrowserSpy.dk executing them automatically . 
---------------------
# How to use 

straightforward e easy to use  : 

- plain exectuon whit no commands as  json as default format ad it save the output in the directory where the code is execute

```Python
python3 BrowserSecTests.py 

```

- Specify format or output directory & file name 

```Python
python3 BrowserSecTests.py -f text -o /path/to/dir/test.txt

```

- as tiny is it check the --help command 

---------

# Compability issues  
as this stage the BST it wokrs only in **Chrome/Chromium** borwsers ( unix env ). it should be works on dos machine if python and releated modules are installed .
**its still in deep devlopemnts and the future upgrade will be focused on the "multi-platform" compability **

----------


Future Upgrade & improvments 

- Firefox & other boweser adaptation
- xml output is a mess ,fixing it out and make it redable  (sincerly i do not why i put it in) 
- Multi-Platform 

i think its all for now

again thanks to : <a href='https://browserspy.dk/'><img alt="BrowserSpy.dk button" width="80" height="15" src="https://browserspy.dk/pics/browserspybutton.jpg" /></a>

