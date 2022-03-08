#include <iostream>
void half_pyramid(int rows){
rows++;
for(int i = 0; i < rows; i++){
for(int j = 0; j < i; j++){
std::cout << "*";;
};
std::cout << "\n";;
};
};
int main(){
half_pyramid(5);
return 0;
};
