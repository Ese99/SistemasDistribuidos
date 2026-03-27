#ifndef UTILS_H
#define UTILS_H

#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <fstream>
#include <string>

// Permite modificar la malla desde la compilación (Bash)
#ifndef VALOR_M
#define VALOR_M 50
#endif
#ifndef VALOR_N
#define VALOR_N 50
#endif

// Tolerancia estricta
const double TOL = 1e-7; 

// Obtiene los límites del dominio según el ejemplo
void get_domain(int ex, double& x_0, double& x_f, double& y_0, double& y_f) {
    if (ex == 1) { x_0=0.0; x_f=2.0; y_0=0.0; y_f=1.0; }
    else if (ex == 2) { x_0=1.0; x_f=2.0; y_0=0.0; y_f=1.0; }
    else if (ex == 3) { x_0=1.0; x_f=2.0; y_0=0.0; y_f=2.0; }
    else if (ex == 4) { x_0=1.0; x_f=2.0; y_0=1.0; y_f=2.0; }
    else { x_0=0.0; x_f=1.0; y_0=0.0; y_f=1.0; } // Fallback de seguridad
}

// Soluciones analíticas exactas (Condiciones de frontera)
double exact_sol(int ex, double x, double y) {
    if (ex == 1) return std::exp(x * y);
    if (ex == 2) return std::log(x * x + y * y);
    if (ex == 3) return (x - y) * (x - y);
    if (ex == 4) return x * y * std::log(x * y);
    return 0.0;
}

// Funciones fuente (Lado derecho de la Ecuación de Poisson)
double source_func(int ex, double x, double y) {
    if (ex == 1) return (x * x + y * y) * std::exp(x * y);
    if (ex == 2) return 0.0;
    if (ex == 3) return 4.0;
    if (ex == 4) return (x / y) + (y / x);
    return 0.0;
}

void initialize_grid(int ex, int M, int N, std::vector<std::vector<double>>& T, double& h, double& k) {
    double x_0 = 0.0, x_f = 0.0, y_0 = 0.0, y_f = 0.0; // Inicializadas
    get_domain(ex, x_0, x_f, y_0, y_f);
    h = (x_f - x_0) / M;
    k = (y_f - y_0) / N;

    T.assign(M + 1, std::vector<double>(N + 1, 0.0));
    
    // Condiciones de frontera exactas
    for (int j = 0; j <= N; ++j) {
        T[0][j] = exact_sol(ex, x_0, y_0 + j * k);
        T[M][j] = exact_sol(ex, x_f, y_0 + j * k);
    }
    for (int i = 0; i <= M; ++i) {
        T[i][0] = exact_sol(ex, x_0 + i * h, y_0);
        T[i][N] = exact_sol(ex, x_0 + i * h, y_f);
    }
}

void get_source_matrix(int ex, int M, int N, std::vector<std::vector<double>>& source, double h, double k) {
    double x_0 = 0.0, x_f = 0.0, y_0 = 0.0, y_f = 0.0; // Inicializadas
    get_domain(ex, x_0, x_f, y_0, y_f);
    source.assign(M + 1, std::vector<double>(N + 1, 0.0));
    for (int i = 0; i <= M; ++i) {
        for (int j = 0; j <= N; ++j) {
            source[i][j] = source_func(ex, x_0 + i * h, y_0 + j * k);
        }
    }
}

void export_to_file(int ex, const std::vector<std::vector<double>>& T, double h, double k, int M, int N, const std::string& method_name) {
    // PROTECCIÓN PARA EL CLÚSTER: Si la malla es muy grande (> 1000), no guardamos el .dat 
    // porque generaría gigabytes de datos y colapsaría el almacenamiento del clúster.
    if (M > 1000) return; 

    double x_0 = 0.0, x_f = 0.0, y_0 = 0.0, y_f = 0.0; // Inicializadas
    get_domain(ex, x_0, x_f, y_0, y_f);
    
    std::string filename = "data/solucion_" + method_name + "_Ej" + std::to_string(ex) + ".dat";
    std::ofstream file(filename);
    if (!file.is_open()) return;
    
    for (int i = 0; i <= M; ++i) {
        for (int j = 0; j <= N; ++j) {
            file << (x_0 + i * h) << "\t" << (y_0 + j * k) << "\t" << T[i][j] << "\n";
        }
    }
    file.close();
}
#endif