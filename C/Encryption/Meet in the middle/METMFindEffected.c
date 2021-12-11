#include <stdio.h>
#include <stdlib.h>

unsigned long int AddRoundkey(unsigned long int res,unsigned long int key){
    return (res | (key & 0x00000000FFFFFFFF));
}

unsigned long int SubCells(unsigned long int res){
    unsigned long int newres=0;
    for(int j=0;j<16;j++){
        newres|=((res>>(j*4)) & 0xF) << (((j/4)*16)+(((j%4)+((15-j)/4))%4)*4);
    }
    return newres;
}
unsigned long int MixColumns(unsigned long int res){
    unsigned long int newres=0;
    unsigned long int row0=((res>>48)&0xFFFF);
    unsigned long int row1=((res>>32)&0xFFFF);
    unsigned long int row2=((res>>16)&0xFFFF);
    unsigned long int row3=res&0xFFFF;
    newres=((row0 | row2)<< 48)|((row1 | row2)<< 32)|((row0 | row3)<< 16)|(row2 | row3);
    return newres;
}

unsigned long int encrypt(unsigned long int input,unsigned long int key){
    unsigned long int res=input,roundkey=key;
    for(int i=0;i<4;i++){
        res=AddRoundkey(res,roundkey&0xFFFFFFFF);
        res=SubCells(res);//+shiftrows
        res=MixColumns(res);
        roundkey=(roundkey>>16)|(roundkey<<48);
    }
    return res;
}

int main(){
    unsigned long int input=0x0,output=0XB8B825255959E1E1,result,check,basekey=0xF,counter=0;
    int k=0,resarr[16]={0};
    unsigned long  int key =basekey;/*making the key*/
    for(int i=0;i<16;i++){
        /*making the key*/
        result=encrypt(input,key);
        printf("The key is %lX\n the res is %lX\n",key,result);
        key = key<<4;
        for(k=0;k<16;k++){
            if((result & 0xF)==0xF)resarr[k]++;
            result=result>>4;
        }
        for(k=0;k<16;k++){
            printf("%d,",resarr[k]);
        }
    }
    
    printf("output=%lX result=%lX check=%d key=%lX\n",output,result,output==result,key);
    return 1; 
}