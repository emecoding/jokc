Thank you downloading jokc!

Jokc is a programming language that is parsed by python to c++ code.
Jokc is also targeted for software development, furher on.

Syntax of Jokc is taken from python, c++ and other popular programming languages.
With this documentation, you will get to know the basic syntax of jokc.

1. Creating the basic jokc project
    To do this, you just need to create a basic file with extension '.jokc'.
    Also create a folder called 'Compiles' to store the c++ files.

2. Hello world
    First step in new programming language is to write basic hello world program.
    To do this you have to create main function, like in c++ and c.
    If you don't have a main function, the g++ compiler (compiler that jokc uses to compile .cpp files to .exe) gives you a error.
    This is how you create a main function in jokc:
        dif main(){
            return 0;
        };
    
    To accomplish the hello world program, type 'print("Hello world!")' just above the return keyword.

    Let's go over what we just did.
    First there is 'dif'. 'dif' is a built in function return type, that returns int.
    Then there is 'main'. It is just the function name.
    '()' are basic syntax in every function after function declaration. Inside those brackets would come some arguments, but here we don't need them.
    After all that there is '{' and '};'. Inside those curly brackets comes everything that is inside the function you are using.

    To compile and run the program, type: 'jokc -f file.jokc -d Compiles/ -o Compiles/test_run' to console.
    Make sure that you have jokc.py file in the same directory as where you are typing the command from.

    Congrats!
    You should see 'Hello World!' popping up from the console!
    
3. Checking out the command
    Understading the command is not hard.
    There is few flags and that's it.
    Let me tell what those flags does.

    jokc is ofcourse the command that parses and compiles the file.
    '-f' tells the parser which file to compile.
    '-d' tells where to put the final c++ file.
    '-o' tells the name of the executable file.

    If you are missing any of those flags, the parser will throw a error at your face.

    In addition there is also '-i' which tells the parser which directorys are being imported. But for now, we don't need that.


    
