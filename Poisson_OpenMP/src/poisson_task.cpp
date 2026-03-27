#include "utils.h"
#include <omp.h>

void solve_poisson(std::vector<std::vector<double>>& T, const std::vector<std::vector<double>>& source, int M, int N, double h, double k) {
    double delta = 1.0;
    int block_size = std::max(10, M / 10); // Escala el bloque dinámicamente
    while (delta > TOL) {
        double max_delta = 0.0;
        #pragma omp parallel shared(max_delta)
        {
            #pragma omp single
            {
                for (int bi = 1; bi < M; bi += block_size) {
                    for (int bj = 1; bj < N; bj += block_size) {
                        #pragma omp task shared(max_delta)
                        {
                            double local_delta = 0.0;
                            for (int i = bi; i < std::min(bi + block_size, M); ++i) {
                                for (int j = bj; j < std::min(bj + block_size, N); ++j) {
                                    double T_new = (((T[i+1][j] + T[i-1][j]) * k*k) + ((T[i][j+1] + T[i][j-1]) * h*h) - (source[i][j] * h*h * k*k)) / (2.0 * (h*h + k*k));
                                    local_delta = std::max(local_delta, std::abs(T_new - T[i][j]));
                                    T[i][j] = T_new;
                                }
                            }
                            #pragma omp critical
                            { max_delta = std::max(max_delta, local_delta); }
                        }
                    }
                }
                #pragma omp taskwait
            }
        }
        delta = max_delta;
    }
}

int main() {
    int M = VALOR_M, N = VALOR_N;
    for (int ex = 1; ex <= 4; ++ex) {
        std::vector<std::vector<double>> T, source; double h, k;
        initialize_grid(ex, M, N, T, h, k); get_source_matrix(ex, M, N, source, h, k);
        solve_poisson(T, source, M, N, h, k);
        export_to_file(ex, T, h, k, M, N, "task");
    }
    return 0;
}