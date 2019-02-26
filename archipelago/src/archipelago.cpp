
// Standard library includes
#include <iostream>
#include <vector>
#include <limits>
#include <sstream>

// Using declarations
using std::cin;
using std::cout;
using std::endl;
using std::string;
using std::vector;

// Code for implementing disjoint sets

class DisjointSets {
    public:
        DisjointSets(unsigned int size);

        // Returns a representative element from the set containing
        // elem.
        int find(int elem);

        // Modifies the data structure to merge the sets containing a
        // and b
        void merge(int a, int b);

    private:
        std::vector<int> parents;
        std::vector<int> ranks;
};

typedef class DisjointSets DisjointSets;

DisjointSets::DisjointSets(unsigned int size) {
    for (int i = 0; i < size; i++) {
        this->parents.push_back(i);
        this->ranks.push_back(0);
    }
}

int DisjointSets::find(int elem) {
    int idx = elem;
    int start_idx = elem;
    int final_idx;

    while (idx != this->parents.at(idx)) {
        idx = this->parents.at(idx);
    }
    final_idx = idx;

    // Now run path compression
    idx = start_idx;
    while (idx != final_idx) {
        int next_idx;
        next_idx = this->parents.at(idx);
        this->parents.at(idx) = final_idx;
        idx = next_idx;
    }

    return final_idx;
}

void DisjointSets::merge(int a, int b) {
    int a_head = this->find(a);
    int b_head = this->find(b);

    if (a_head == b_head)
        return;

    if (this->ranks.at(a_head) < this->ranks.at(b_head)) {
        int tmp = a_head;
        a_head = b_head;
        b_head = tmp;
    }
    this->parents.at(b_head) = a_head;

    if (this->ranks.at(a_head) == this->ranks.at(b_head))
        this->ranks.at(a_head)++;
}

int main() {
    // Read in input
    int N; // number of lines in input
    int m; // number of islands
    cin >> N;
    cin >> m;
    cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    DisjointSets sets(m); // Initialize disjoint sets data structure

    for (string line; std::getline(cin, line); ) { // Loop over lines of input
        std::istringstream sline(line);
        char line_type;
        int arg1;
        int arg2;
        int q_result = -1;

        sline.get(line_type);
        sline >> arg1 >> arg2;
        if (line_type == 'B') {
            cout << "Building ";
            sets.merge(arg1, arg2);
        } else if (line_type == 'Q') {
            cout << "Querying ";
            if (sets.find(arg1) == sets.find(arg2))
                q_result = 1;
            else
                q_result = 0;
        } else {
            cout << "Unknown instruction ";
        }
        cout << arg1 << " " << arg2 << endl;
        if (q_result != -1)
            cout << "Result: " << ((q_result == 1) ? "y" : "n") << endl;
    }

    return 0;
}
