#include "utils.h"
#include <omp.h>

void solve_poisson(std::vector<std::vector<double>>& T, const std::vector<std::vector<double>>& source, int M, int N, double h, double k, int ex) {
    double delta = 1.0;
    int iterations = 0;
    while (delta > TOL) {
        delta = 0.0;
        #pragma omp parallel for collapse(2) reduction(max:delta)
        for (int i = 1; i < M; ++i) {
            for (int j = 1; j < N; ++j) {
                double T_new = (((T[i+1][j] + T[i-1][j]) * k*k) + ((T[i][j+1] + T[i][j-1]) * h*h) - (source[i][j] * h*h * k*k)) / (2.0 * (h*h + k*k));
                delta = std::max(delta, std::abs(T_new - T[i][j]));
                T[i][j] = T_new;
            }
        }
        #pragma omp atomic
        iterations++;
    }
    if(M <= 1000) std::cout << "Ej " << ex << " Iteraciones (Atomic): " << iterations << std::endl;
}

int main() {
    int M = VALOR_M, N = VALOR_N;
    for (int ex = 1; ex <= 4; ++ex) {
        std::vector<std::vector<double>> T, source; double h, k;
        initialize_grid(ex, M, N, T, h, k); get_source_matrix(ex, M, N, source, h, k);
        solve_poisson(T, source, M, N, h, k, ex);
        export_to_file(ex, T, h, k, M, N, "atomic");
    }
    return 0;
}