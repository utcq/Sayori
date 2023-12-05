#include <stdint.h>
#include "main.h"

#include <stdio.h>
uint16_t n1;

int add(int x, int y) {
	return ((x-1)+y);
}

int* main() {
	char* greet = "Hello";
	int num = add((1+80), 32);
	printf("%s\n", greet);
	return 0;
}

