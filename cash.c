#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{

    float change;
    int coins = 0;
    int remain = 0;

//Prompting the user for input. Value should be positive
    do
    {
        change = get_float("Change: "); 
    }
    while (change <= 0);

//Multiply dollars by 100 and round cents to nearest penny
    int cents = (int)change;
    cents = round(change * 100);

    remain = cents;
//case 25
    coins = cents / 25;
    remain = cents % 25;
//case 10
    coins = coins + (remain / 10);
    remain = remain % 10;
//case 5
    coins = coins + (remain / 5);
    remain = remain % 5;
//case 1  
    coins += remain;

    printf("%i\n", coins);
}
