#include <iostream>              // Includes the standard input/output stream library for C++
#include <vector>               // Includes the vector library for using dynamic arrays
using namespace std;             // Allows you to use names from the std namespace without prefixing them with 'std::'

/*
int main() {                     // Main function: program execution starts here
    std::cout << "Hello, World!" << std::endl; // Prints "Hello, World!" to the console, then ends the line
    return 0;                    // Returns 0 to the operating system, indicating successful completion
}
*/

// Original ArrayModifier class
class ArrayModifier {
public:
    // Method that adds 1 to each element of the array
    void addOne(float arr[], int size) {
        for (int i = 0; i < size; ++i) {
            arr[i] += 1;
        }
    }
};

// Cleaner, more idiomatic C++ class
class ArrayModifierClean {
private:
    vector<float> vec; // Member variable to store the array

public:
    // Constructor to initialize the array
    ArrayModifierClean(const vector<float>& input) : vec(input) {}

    // Method to add 1 to each element
    void addOne() {
        for (float& num : vec) {
            num += 1;
        }
    }

    // Method to print the array
    void print() const {
        for (float num : vec) {
            cout << num << " ";
        }
        cout << endl;
    }
};

int main() {
    // Using the original ArrayModifier class
    float numbers[] = {2.5, 3.0, 4.5};
    int size = sizeof(numbers) / sizeof(numbers[0]);

    ArrayModifier modifier;
    modifier.addOne(numbers, size);

    cout << "Modified array (original class): ";
    for (int i = 0; i < size; ++i) {
        cout << numbers[i] << " ";
    }
    cout << endl;

    // Using the cleaner ArrayModifierClean class
    vector<float> numbersVec = {2.5, 3.0, 4.5};
    ArrayModifierClean cleanModifier(numbersVec);

    cleanModifier.addOne();
    cout << "Modified array (clean class): ";
    cleanModifier.print();

    return 0;
}

