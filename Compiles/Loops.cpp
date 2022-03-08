#include <string>
#include <iostream>
void p(std::string text,int j){
for(int i = 0; i < 10; i++){
std::cout << text << std::endl;
};
};
int main(){
std::string text = "TEST";
p("text", 1);
return 0;
};


