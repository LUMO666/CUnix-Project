#include<iostream>

using namespace std;

class fraction {
public:
    int numerator; //分子
    int denominator;    //分母
    fraction(int n, int d);
    fraction operator+ (const fraction& f2){
        return fraction(numerator+f2.numerator, denominator+f2.denominator);
    }
    fraction operator- (const fraction& f2){
        return fraction(numerator-f2.numerator, denominator-f2.denominator);
    }
    fraction operator* (const fraction& f2){
        return fraction(numerator*f2.numerator, denominator*f2.denominator);
    }
    fraction operator/ (const fraction&f2){
        return fraction(numerator*f2.denominator, denominator*f2.numerator);
    }
    fraction simp(){
        int x = numerator;
        int y = denominator;
        int z = y;
        while(x%y!=0){
            z=x%y;
            x=y;
            y=z;
        }
        return fraction(numerator/z, denominator/z);
    }
    float fr_float(){
        float n = numerator;
        float d = denominator;
        return (n/d);
    }
    void display(){
        cout<<numerator<<"/"<<denominator<<endl;
    }
};

fraction::fraction(int n,int d){
    numerator=n;
    denominator=d;
}

int main(){
    fraction f1(4,5);
    fraction f2(5,8);
    (f1+f2).display();
    (f1-f2).display();
    (f1*f2).display();
    (f1/f2).display();
    (f1*f2).simp().display();
    cout<<(f1/f2).fr_float()<<endl;
    return 0;
}