#include <iostream>
void FOR_LOOP(int j){
for(int i = 0; i < 10; i++){
int s = i+j*i;
std::cout << s << std::endl;
};
};
void WHILE_LOOP(int start_i,int end_i){
int i = start_i;
while(i<end_i){
FOR_LOOP(i);
i++;
};
};
int main(){
WHILE_LOOP(0, 100);
return 0;
};


