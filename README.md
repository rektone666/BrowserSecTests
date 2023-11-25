# BrowserSecTests
BrowserSecTests is just a small python experiment tool for lazy people like me which automatically execute a series of security test of your browser .
those test are focused to check how and what data can or cannot be retrived from our browser by simply visiting a page . 
it goes through 75 differts test , from VBScript, COOKIES and so on ... 
the code works around BrowserSpy.dk executing them automatically . 
---------------------
# How to use 

On this version there is no more to run requirements.txt since BTS do it for you 


execution remain the same   : 

- plain exectuon whit no commands as  json as default format ad it save the output in the directory where the code is execute

```bash
python3 BrowserSecTests.py 

```

- Specify format or output directory & file name 

```bash
python3 BrowserSecTests.py -f text -o /path/to/dir/test.txt

```

- as tiny is it check the --help command 

---------

# Compability issues  
BTS V2 should work whit no problem in windows and any linux distro and actually support CHROME/CHROMIUM , FIREFOX & INTERENT explorer . 
If you have missing driver of your browser BTS should fix that and install the appropiate driver whit all the modules he needed .
- YES IT ASK for permission if u want proceed
- it wil create even a requirements.txt so if BTS has  any problem to install modules and divers needed u can stil use the good old requirements  
----------

Future Upgrade & improvments 

the priority for now it slow down on this version and make improvements on this about since i had still to do tons of tests 

then , if the projecet as a bit of sense : 

- Mac compatibility
- Try to make compatibile whit other popular browsers like safari or opera 
- ? 

again thanks to : <a href='https://browserspy.dk/'><img alt="BrowserSpy.dk button" width="80" height="15" src="https://browserspy.dk/pics/browserspybutton.jpg" /></a>

