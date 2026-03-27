#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <string>

using namespace std;

int main(int argc, char* argv[]) {
    if (argc != 4) {
        cerr << "Uso: ./Iman_GS <tamanio_malla> <iteraciones> <sufijo_archivo>" << endl;
        return 1;
    }
    
    int IMAX = stoi(argv[1]);
    int JMAX = IMAX;
    int max_iters = stoi(argv[2]);
    string suffix = argv[3];

    vector<vector<double>> PHI(IMAX + 1, vector<double>(JMAX + 1));
    vector<vector<int>> FLAG(IMAX + 1, vector<int>(JMAX + 1));

    double M, PI, V, H;
    int I1, I2, J1;

    PI = 4.0 * atan(1.0);
    H = 1.0;
    I1 = 6 * 5;  // 30
    I2 = 15 * 5; // 75
    J1 = 4 * 5;  // 20
    M = 1000.0;
    V = 10.0;

    // DEFINICIÓN DE FLAG (Restaurada estructura original)
    for (int i = 2; i < IMAX; ++i) {
        for (int j = 2; j < JMAX; ++j) {
            FLAG[i][j] = 0;
        }
    }
    for (int i = 1; i <= IMAX; ++i) FLAG[i][1] = 1;
    for (int i = 1; i <= IMAX; ++i) FLAG[i][JMAX] = 2;
    for (int j = 2; j < JMAX; ++j) FLAG[IMAX][j] = 3;
    for (int j = 2; j < JMAX; ++j) FLAG[1][j] = 4;
    for (int j = 2; j < J1; ++j) {
        FLAG[I1][j] = 5;
        FLAG[I2][j] = 5;
    }
    for (int i = I1 + 1; i < I2; ++i) FLAG[i][J1] = 6;
    FLAG[I1][J1] = 7;
    FLAG[I2][J1] = 7;

    // INICIALIZACIÓN DE PHI (Restaurada estructura original)
    for (int i = 1; i <= IMAX; ++i) {
        for (int j = 1; j <= JMAX; ++j) {
            PHI[i][j] = 1.0;
        }
    }
    for (int i = 1; i <= IMAX; ++i) PHI[i][1] = 0.0;
    for (int i = 1; i <= IMAX; ++i) PHI[i][JMAX] = (V * M) / (4.0 * PI * pow(i * H, 3));
    for (int j = 1; j <= JMAX; ++j) PHI[IMAX][j] = (V * M) / (4.0 * PI * pow(IMAX * H, 3));

    // SOLUCIÓN POR MÉTODO DE GAUSS-SEIDEL
    for (int icount = 0; icount < max_iters; ++icount) {
        for (int i = 1; i < IMAX; ++i) {
            for (int j = 1; j < JMAX; ++j) {
                double nuevo = 0.0;

                if (FLAG[i][j] == 0) {
                    double A = 1.0 + 1.0 / (2.0 * (double)i);
                    double B = 1.0 - 1.0 / (2.0 * (double)i);
                    nuevo = (A * PHI[i + 1][j] + B * PHI[i - 1][j] + PHI[i][j + 1] + PHI[i][j - 1]) / 4.0;
                }
                else if (FLAG[i][j] == 1 || FLAG[i][j] == 2 || FLAG[i][j] == 3) nuevo = PHI[i][j];
                else if (FLAG[i][j] == 4) nuevo = (4.0 * PHI[2][j] + PHI[1][j + 1] + PHI[1][j - 1]) / 6.0;
                else if (FLAG[i][j] == 5) nuevo = (PHI[i + 1][j] + PHI[i - 1][j]) / 2.0;
                else if (FLAG[i][j] == 6) nuevo = (M * H + PHI[i][j + 1] + PHI[i][j - 1]) / 2.0;
                else if (FLAG[i][j] == 7) nuevo = (M * H + PHI[i][j + 1] + PHI[i][j - 1] + PHI[i + 1][j] + PHI[i - 1][j]) / 4.0;

                PHI[i][j] = nuevo; 
            }
        }
    }

    // SALIDAS (POT-MAG, CAMPO-H, CAMPO-B con i+=5 constante)
    ofstream outPot("POT-MAG_" + suffix + ".dat");
    for (int i = 1; i <= IMAX; ++i) {
        for (int j = 1; j <= JMAX; ++j) {
            outPot << i << " " << j << " " << PHI[i][j] << endl;
        }
        outPot << endl;
    }
    outPot.close();

    ofstream outH("CAMPO-H_" + suffix + ".dat");
    for (int i = 2; i < IMAX; i += 5) {
        for (int j = 2; j < JMAX; j += 5) {
            outH << i << " " << j << " " 
                 << (PHI[i + 1][j] - PHI[i - 1][j]) / (H * 2.0) << " "
                 << (PHI[i][j + 1] - PHI[i][j - 1]) / (H * 2.0) << endl;
        }
        outH << endl;
    }
    outH.close();

    ofstream outB("CAMPO-B_" + suffix + ".dat");
    for (int i = 2; i < IMAX; i += 5) {
        for (int j = 2; j < JMAX; j += 5) {
            double AA = 0.0;
            if (i >= I1 && i <= I2 && j <= J1) AA = M;

            outB << i << " " << j << " "
                 << -(PHI[i + 1][j] - PHI[i - 1][j]) / (H * 2.0) << " "
                 << AA - (PHI[i][j + 1] - PHI[i][j - 1]) / (H * 2.0) << endl;
        }
        outB << endl;
    }
    outB.close();

    return 0;
}