#include <stdio.h>
#include <stdlib.h>


unsigned long int SubCells(unsigned long int res){
    unsigned long int newres=0;
    const unsigned long int sbox[]={0xA,0x5,0x4,0x2,0x6,0x1,0xF,0x3,0xB,0xE,0x7,0x0,0X8,0xD,0xC,0x9};
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

unsigned long int encrypt(unsigned long int input,unsigned long int basekey){
    unsigned long int res=input,roundkey=basekey;
    for(int i=0;i<4;i++){
        res^=(roundkey & 0x00000000FFFFFFFF);//round key
        res=SubCells(res);//+shiftrows
        res=MixColumns(res);
        roundkey=(roundkey>>16)|((roundkey^0xF3F3)<<48);/*maybe |*/
    }
    return res;
}

void *threadwork(void *args){
    long int threadnum = *((int *)args);
    printf("created thread %ld",threadnum);

}
int main(){
    unsigned long int input=0x11C1082590A7136F,output=0X6D0ABBB0C3B0AEBA,result=0,check,key=(0x0000000000),counter=0,cankey=0,k,thekey;
    for(key;(key<0x10000000000);key++){
        unsigned long  int cankey = ((key & 0xFFF) | ((key & 0xFFFF000) << 8) | ((key & 0xFFF0000000) << 12));/*making the key*/
        result=encrypt(input,cankey);
        if(key%0x1000000000==0) printf("the key is %lX,the cankey is %lX\n",key,cankey);
        if((result&0xF00000000000)==(output&0xF00000000000)){//check the nibble
        if((encrypt(0x411E1ACB4B874D01,cankey)&0xF00000000000)==0xE00000000000){
                if((encrypt(0x43F40EFA316F7C83,cankey)&0xF00000000000)==0x600000000000){
                    if((encrypt(0xA693EB8B336103EC,cankey)&0xF00000000000)==0xA00000000000){
                        if((encrypt(0x84587AB1F0247732,cankey)&0xF00000000000)==0x800000000000){
                            if((encrypt(0x12DBCC19188160B0,cankey)&0xF00000000000)==0x400000000000){
                                if((encrypt(0x18A04716625893F3,cankey)&0xF00000000000)==0xD00000000000){
                                    if((encrypt(0xDF00A5D579B7BD71,cankey)&0xF00000000000)==0xC00000000000){
                                        if((encrypt(0x55B22547FC74CAFB,cankey)&0xF00000000000)==0x800000000000){
                                            if((encrypt(0xF7A3C2D6DB001B24,cankey)&0xF00000000000)==0x600000000000){
                                                if((encrypt(0x3C83C16A0F2EA296,cankey)&0xF00000000000)==0xC00000000000){
                                                    if((encrypt(0x1BFEF5F584572E69,cankey)&0xF00000000000)==0x800000000000){
                                                        if((encrypt(0x87AE57992D849B7C,cankey)&0xF00000000000)==0x500000000000){
                                                            if((encrypt(0x12AC32553D6D7EEA,cankey)&0xF00000000000)==0x400000000000){
                                                                if((encrypt(0xC773F25EC7127285,cankey)&0xF00000000000)==0x600000000000){
                                                                    if((encrypt(0x3904BA736843BECF,cankey)&0xF00000000000)==0xA00000000000){
                                                                        printf("entered here with key %lX\n",cankey);
                                                                         for(k=0;k<=0xFFFFFF;k++){
         cankey=((key & 0xFFF) | ((key & 0xFFFF000) << 8) | ((key & 0xFFF0000000) << 12))|((k & 0xFF)<<12)|((k & 0xF00)<<28)|((k & 0xFFF000)<<40);
         result=encrypt(input,cankey);
        if(result==output){
            printf("the key is %lX result %lX\n",cankey,result);
            thekey=cankey;
        }
    }
                                                                       
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }

                        }

                    }
                }
            }
        }
    }
    return 1; 
}