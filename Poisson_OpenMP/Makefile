# ---------------------------------------------------------------------------
# Configuración del compilador y directorios
# ---------------------------------------------------------------------------
CXX      := g++
# Es vital mantener -fopenmp para que el paralelismo funcione
CXXFLAGS := -std=c++17 -O3 -Wall -Wextra -fopenmp -Iinclude

BIN_DIR  := bin
SRC_DIR  := src
DATA_DIR := data
IMAG_DIR := imag
DOC_DIR  := documents

# Encuentra todos los .cpp y genera los nombres de los ejecutables
SRCS := $(wildcard $(SRC_DIR)/*.cpp)
EXES := $(patsubst $(SRC_DIR)/%.cpp, $(BIN_DIR)/%, $(SRCS))

MKDIR_P  := mkdir -p

.PHONY: all run view clean directories docs

all: directories $(EXES)

directories:
	$(MKDIR_P) $(BIN_DIR) $(DATA_DIR) $(IMAG_DIR) $(DOC_DIR)

# Regla de compilación genérica para los 5 archivos
$(BIN_DIR)/%: $(SRC_DIR)/%.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

# ---------------------------------------------------------------------------
# Ejecución y Benchmark de tiempos
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Ejecución y Benchmark de tiempos
# ---------------------------------------------------------------------------
run: all
	@echo "========================================"
	@echo "Preparando el entorno de pruebas..."
	@chmod +x scripts/benchmark.sh
	@./scripts/benchmark.sh
	@echo "========================================"

# ---------------------------------------------------------------------------
# Generación de gráficas
# ---------------------------------------------------------------------------
view:
	@echo "Generando gráficas en 3D..."
	python3 scripts/graficas.py

# ---------------------------------------------------------------------------
# Limpieza
# ---------------------------------------------------------------------------
clean:
	rm -rf $(BIN_DIR) $(DATA_DIR) $(IMAG_DIR)
	rm -rf $(DOC_DIR)/doc_output
	rm -rf $(DOC_DIR)/*.pdf

# ---------------------------------------------------------------------------
# Documentación técnica (Doxygen + LaTeX → PDF)
# ---------------------------------------------------------------------------
docs:
	doxygen $(DOC_DIR)/Doxyfile
	@cd  documents/doc_output/latex && make
	@echo "✅ Documentación generada en: $(DOC_DIR) /documents/doc_output/latex/refman.pdf"
	@cp documents/doc_output/latex/refman.pdf documents/Poisson_OpenMP.pdf
	@echo "📄 Copiado como Poisson_OpenMP.pdf en la carpeta documents$(DOC_DIR)"
	@xdg-open documents/Poisson_OpenMP.pdf > /dev/null 2>&1 &