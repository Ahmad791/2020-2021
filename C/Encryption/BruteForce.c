#include <stdio.h>
#include <stdlib.h>

const unsigned long int input=0xBF2727D9304D0393;
const unsigned long int sbox[16] = {0x2, 0x4, 0x5, 0x6, 0x1, 0xA, 0xF, 0x3,0xB , 0xE , 0x0 , 0x7 , 0x9 , 0x8 , 0xC , 0xD},rounds=20;
const int word_size =64;

unsigned long int power(int x,int y){
unsigned long int r=1;
for(int j=0;j<y;j++){
    r*=x;
}
return r;
}

 unsigned long int rotate_left(unsigned long int word ,int n){
 unsigned long int mask = (unsigned long int)(power(2, word_size)-1);
 return  (((word  << n) & mask) | ((word  >> (word_size  - n) & mask)));
 }

unsigned long int apply_sbox(unsigned long int res){
unsigned long int newres = 0;
        newres|=sbox[(res>>0) & 0xF] << 0;
        newres|=sbox[(res>>4) & 0xF] << 4;
        newres|=sbox[(res>>8) & 0xF] << 8;
        newres|=sbox[(res>>12) & 0xF] << 12;
        newres|=sbox[(res>>16) & 0xF] << 16;
        newres|=sbox[(res>>20) & 0xF] << 20;
        newres|=sbox[(res>>24) & 0xF] << 24;
        newres|=sbox[(res>>28) & 0xF] << 28;
        newres|=sbox[(res>>32) & 0xF] << 32;
        newres|=sbox[(res>>36) & 0xF] << 36;
        newres|=sbox[(res>>40) & 0xF] << 40;
        newres|=sbox[(res>>44) & 0xF] << 44;
        newres|=sbox[(res>>48) & 0xF] << 48;
        newres|=sbox[(res>>52) & 0xF] << 52;
        newres|=sbox[(res>>56) & 0xF] << 56;
        newres|=sbox[(res>>60) & 0xF] << 60;
    return newres;
}



unsigned long int encrypt(unsigned long int key){
unsigned long int word=input,r_key=key;
for(int k=0;k<20;k++){
word ^=r_key;
word = apply_sbox(word);
word= rotate_left(word , 15) ^ rotate_left(word , 32) ^ word;
r_key=rotate_left(r_key , 15) ^ rotate_left(r_key , 32) ^ r_key^0x3;
}
return word;
}


int main()
{
    unsigned long int key=0x20000000,output=0xDC403AF030A9F45B;
    int counter=0,flag=0;
    unsigned long int res;    ;
    for(key=0;key<0x20000000;key++,counter++){
        res=encrypt(key);
        if(res==output) {
            printf("the key is %lX\n",key);
            flag=1;
        }
        if(counter==0x1000000){
        counter=0;
        printf("%lX\n",key);
        }
    }
    if (flag==0)printf("Error\n");
    return 1;
}
