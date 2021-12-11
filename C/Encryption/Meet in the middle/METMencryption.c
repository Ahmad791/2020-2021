#include <stdio.h>
#include <stdlib.h>

const unsigned long int sbox[]={0xA,0x5,0x4,0x2,0x6,0x1,0xF,0x3,0xB,0xE,0x7,0x0,0X8,0xD,0xC,0x9};
unsigned long int SubCells(unsigned long int res){
    unsigned long int newres=0;
        /*newres|=sbox[(res>>(j*4)) & 0xF] << (((j/4)*16)+(((j%4)+((15-j)/4))%4)*4); possible optimization*/
        newres|=sbox[(res>>0) & 0xF] << 12;
        newres|=sbox[(res>>4) & 0xF] << 0;
        newres|=sbox[(res>>8) & 0xF] << 4;
        newres|=sbox[(res>>12) & 0xF] << 8;
        newres|=sbox[(res>>16) & 0xF] << 24;
        newres|=sbox[(res>>20) & 0xF] << 28;
        newres|=sbox[(res>>24) & 0xF] << 16;
        newres|=sbox[(res>>28) & 0xF] << 20;
        newres|=sbox[(res>>32) & 0xF] << 36;
        newres|=sbox[(res>>36) & 0xF] << 40;
        newres|=sbox[(res>>40) & 0xF] << 44;
        newres|=sbox[(res>>44) & 0xF] << 32;
        newres|=sbox[(res>>48) & 0xF] << 48;
        newres|=sbox[(res>>52) & 0xF] << 52;
        newres|=sbox[(res>>56) & 0xF] << 56;
        newres|=sbox[(res>>60) & 0xF] << 60;
    return newres;
}
unsigned long int MixColumns(unsigned long int res){
    unsigned long int newres=0;
    unsigned long int row0=((res>>48)&0xFFFF);
    unsigned long int row1=((res>>32)&0xFFFF);
    unsigned long int row2=((res>>16)&0xFFFF);
    unsigned long int row3=res&0xFFFF;
    newres=((row0 ^ row2)<< 48)|((row1 ^ row2)<< 32)|((row0 ^ row3)<< 16)|(row2 ^ row3);
    return newres;
}

unsigned long int encrypt(unsigned long int input,unsigned long int key){
    unsigned long int res=input,roundkey=key;
    for(int i=0;i<10;i++){
        res^=(roundkey & 0x00000000FFFFFFFF);//round key
        res=SubCells(res);//+shiftrows
        res=MixColumns(res);
        roundkey=(roundkey>>16)|((roundkey^0xF3F3)<<48);/*maybe |*/
    }
    return res;
}

int main(){
    unsigned long int input=0x000000000000000,output=0X65DC865A2A284FF4,result=0,check,key=0x0000000000000,counter=0;
    //for(key;(key<0xF00000000)&&(result!=output);key++){
        result=encrypt(input,key);
    //}
    
    printf("output=%lX result=%lX check=%d key=%lX\n",output,result,output==result,key-1);
    return 1; 
}