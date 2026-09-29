#include <iostream>
#include <random>
#include <vector>
#include <string>

int main() {
    std::mt19937 rng(static_cast<unsigned int>(std::random_device{}()));
    std::uniform_int_distribution<int> stepDist(0, 1);

    const int steps = 10;
    std::vector<int> positions(steps + 1);
    positions[0] = 0;

    for (int i = 1; i <= steps; ++i) {
        int step = stepDist(rng) == 0 ? -1 : 1;
        positions[i] = positions[i - 1] + step;
    }

    int minPos = positions[0];
    int maxPos = positions[0];
    for (int pos : positions) {
        if (pos < minPos) minPos = pos;
        if (pos > maxPos) maxPos = pos;
    }

    int width = maxPos - minPos + 1;
    std::cout << "Random walk positions:\n";
    for (int i = 0; i <= steps; ++i) {
        std::cout << "Step " << i << ": " << positions[i] << "\n";
    }

    std::cout << "\nASCII plot:\n";
    for (int i = 0; i <= steps; ++i) {
        int offset = positions[i] - minPos;
        std::string line(width, ' ');
        line[offset] = '*';
        std::cout << line << "  (" << positions[i] << ")\n";
    }

    return 0;
}