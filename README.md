---

# **Reconhecimento de Gestos - Libras**
Este projeto implementa um sistema de reconhecimento de gestos utilizando as bibliotecas **OpenCV** e **MediaPipe**. O sistema é capaz de identificar gestos de uma ou duas mãos e exibir os resultados em tempo real, ajudando no reconhecimento de gestos usados na linguagem de sinais ou interações gestuais.

---

## **Funcionalidades**
- **Detecção de mãos:** Utiliza o MediaPipe para identificar as mãos na imagem.
- **Reconhecimento de gestos simples:** Detecta gestos como "Oi", "Sim", "Não", "Eu te amo", entre outros.
- **Combinação de gestos:** Detecta combinações de gestos com duas mãos, como "Paz e Amor" ou "Rock and Roll".
- **Suavização da detecção:** Utiliza uma fila para evitar falsos positivos e tornar as detecções mais estáveis.

---

## **Requisitos**
### Dependências do Python
Certifique-se de ter o Python instalado. As dependências podem ser instaladas com:
```bash
pip install opencv-python mediapipe
```

---

## **Como executar o projeto**
1. Clone o repositório ou copie o código para seu ambiente local:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <PASTA_DO_REPOSITORIO>
   ```

2. Execute o script Python:
   ```bash
   python reconhecimento_gestos.py
   ```

3. Certifique-se de que uma câmera está conectada e funcionando. A janela de vídeo será exibida.

4. Para encerrar a aplicação, pressione a tecla **'q'**.

---

## **Gestos Reconhecidos**
### **Gestos com uma mão:**
| Gesto               | Dedos Levantados       | Descrição                |
|---------------------|------------------------|--------------------------|
| **Oi**              | `[0, 1, 0, 0, 0]`     | Apenas o indicador       |
| **Mão aberta**      | `[0, 1, 1, 1, 1]`     | Todos exceto o polegar   |
| **Eu te amo**       | `[1, 1, 1, 0, 0]`     | Polegar, indicador e médio |
| **Não**             | `[0, 0, 0, 0, 0]`     | Nenhum dedo levantado    |
| **Sim**             | `[1, 0, 0, 0, 0]`     | Apenas o polegar         |
| **Paz**             | `[1, 1, 0, 0, 0]`     | Polegar e indicador      |
| **Rock**            | `[0, 0, 0, 1, 1]`     | Anelar e mínimo          |

### **Gestos combinados com duas mãos:**
| Gesto               | Combinação             | Descrição                |
|---------------------|------------------------|--------------------------|
| **Bater palmas**    | Mão aberta + Mão aberta | Duas mãos abertas        |
| **Aprovação dupla** | Sim + Sim              | Dois polegares levantados|
| **Amor recíproco**  | Eu te amo + Eu te amo  | Amor expresso em ambas as mãos |

---

## **Contribuições**
Contribuições são bem-vindas! Sinta-se à vontade para abrir um *pull request* ou relatar problemas na seção de *issues*.

---

## **Licença**
Este projeto está licenciado sob a [Licença MIT](LICENSE).  

---

## **Capturas de Tela (Opcional)**
Adicione imagens ou GIFs do sistema em execução para ilustrar os resultados.

---
