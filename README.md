# Navegação Autônoma e Mapeamento Batimétrico com WAM-V (ROS 2 & Gazebo VRX)

Este repositório contém a implementação completa do sistema de controle, fusão de sensores, navegação autônoma e mapeamento batimétrico em tempo real para o veículo de superfície autônomo **WAM-V**, simulado no ambiente **VRX (Virtual Robotx)** sobre **ROS 2** e **Gazebo Sim**.

---

## 🚀 Funcionalidades Principais

1. **Fusão de Sensores e Estimativa de Pose (EKF):**
   * Fusão de dados de IMU e GPS (NavSat) via Filtro de Kalman Estendido (`robot_localization`) garantindo pose absoluta e contínua do veículo em mar aberto.
   * Resolução automática de instabilidades nas articulações físicas dos propulsores em tempo de execução via correção de URDF.
2. **Navegação Global e Local (Nav2):**
   * Configuração robusta de mapas de custo globais e locais (`local_costmap` e `global_costmap` em janela deslizante de 200m x 200m).
   * Seguimento autônomo de waypoints em padrão de slalom/zigue-zague para varredura de área.
   * Algoritmo de controle local Pure Pursuit Regregulado para manobras de curvas suaves na água.
3. **Mapeamento Batimétrico (Sonar Virtual):**
   * Nó de batimetria virtual simulando um ecobatímetro a **20Hz** a partir de mapas de elevação realísticos do leito marinho.
   * Nó de mapeamento em tempo real interpolando medições acústicas e gerando a imagem consolidada do relevo submarino (`bathymetry_map.png`).
4. **Interface e Segurança:**
   * Listener de terminal para cancelamento seguro e geração imediata do mapa ao pressionar a tecla `F`.

---

## 📂 Estrutura do Repositório

* **`src/robmov_slam/`**: Pacote ROS 2 principal contendo:
  * **`launch/`**: Launch files do sistema de navegação e localização (`slam_localization.launch.py` e `navigation_launch.py`).
  * **`config/`**: Parâmetros do filtro EKF (`ekf_config.yaml`) e do Nav2 (`nav2_params.yaml`).
  * **`src/`**: Nós Python de missão (`mission_coverage.py`), sonar (`software_bathymetry.py`), mapeamento (`bathymetry_mapper.py`) e tradução cinemática (`twist2thrust.py`).
* **`run_all.sh`**: Script para iniciar a simulação completa com interface gráfica (Gazebo + RViz + Missão).
* **`run_sim.sh`**: Script otimizado que inicia a simulação em modo **headless** (ideal para ambientes com restrição de CPU/RAM).
* **`tracker.py`**: Utilitário para rastreamento e gravação da pose real executada.

---

## 🛠️ Como Instalar e Rodar

### Pré-requisitos
* ROS 2 Jazzy Jalisco
* Gazebo Sim Harmonic
* Dependências do VRX configuradas

### Instalação
Clone o repositório no seu ambiente de desenvolvimento e compile o workspace:
```bash
# Navegar até a raiz do repositório clonado
cd vrx-gazebo

# Compilar o workspace colcon
colcon build

# Carregar o ambiente do workspace
source install/setup.bash
```

### Executando a Missão Completa
Para iniciar a simulação gráfica, a stack de navegação e a missão de cobertura automaticamente:
```bash
./run_all.sh
```

Para rodar de forma otimizada sem a interface gráfica do Gazebo (Headless):
```bash
./run_sim.sh
```

---

## 📊 Resultados e Logs

* Os arquivos de log detalhados de cada subsistema (Gazebo, Nav2, sensores, etc.) são armazenados automaticamente no diretório `log/` para manter a raiz limpa.
* O mapa batimétrico final é gravado na raiz do projeto como `bathymetry_map.png`.
