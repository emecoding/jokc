#include <iostream>
void half_pyramid(int rows){
int r1 = rows+1;
for(int i = 1; i < r1; i++){
int r2 = i+1;
for(int j = 1; j < r2; j++){
std::cout << "*";;
};
std::cout << "\n";;
};
};
int main(){
half_pyramid(5);
return 0;
};
