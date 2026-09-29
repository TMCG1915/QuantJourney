#include <bits/stdc++.h>
using namespace std;

int minFountains(const vector<int>& locations) {
    int n = (int)locations.size();
    if (n == 0) return 0;

    vector<int> maxReach(n, 0);

    for (int i = 0; i < n; ++i) {
        int left = max(0, i - locations[i]);
        int right = min(n - 1, i + locations[i]);
        maxReach[left] = max(maxReach[left], right);
    }

    int activated = 0;
    int currentEnd = 0;
    int furthest = 0;

    for (int i = 0; i < n; ++i) {
        furthest = max(furthest, maxReach[i]);

        if (i == currentEnd) {
            if (furthest <= i) return -1; // can't advance
            ++activated;
            currentEnd = furthest;
            if (currentEnd >= n - 1) return activated;
        }
    }

    return activated;
}

int main() {
    vector<int> locations = {0,2,1,2,1,3,1};
    cout << minFountains(locations) << '\n';
    return 0;
}
