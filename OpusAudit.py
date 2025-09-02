
import sys
import os
import threading

# Adds ADB to the PATH automatically 
adb_path = r"C:\platform-tools"
if adb_path not in os.environ.get("PATH", ""):
    os.environ["PATH"] += f";{adb_path}"
    
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
                             QHBoxLayout, QSpinBox, QTextEdit, QMessageBox, QCheckBox, QLineEdit, QComboBox)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer

class OpusAuditApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpusAudit - Whatsapp Audio Leak")
        self.setGeometry(200, 200, 700, 680)
        self.setStyleSheet("background-color: black; color: white;")

        self.layout = QVBoxLayout()
        self.banner = QLabel()
        self.banner.setPixmap(QPixmap("logo.png").scaledToWidth(400, Qt.SmoothTransformation))
        self.banner.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.banner)

        ascii_banner = QLabel()
        ascii_banner.setText("""
    ░█████╗░██████╗░██╗░░░██╗░██████╗░█████╗░██╗░░░██╗██████╗░██╗████████╗
    ██╔══██╗██╔══██╗██║░░░██║██╔════╝██╔══██╗██║░░░██║██╔══██╗██║╚══██╔══╝
    ██║░░██║██████╔╝██║░░░██║╚█████╗░███████║██║░░░██║██║░░██║██║░░░██║░░░
    ██║░░██║██╔═══╝░██║░░░██║░╚═══██╗██╔══██║██║░░░██║██║░░██║██║░░░██║░░░
    ╚█████╔╝██║░░░░░╚██████╔╝██████╔╝██║░░██║╚██████╔╝██████╔╝██║░░░██║░░░
    ░╚════╝░╚═╝░░░░░░╚═════╝░╚═════╝░╚═╝░░╚═╝░╚═════╝░╚═════╝░╚═╝░░░╚═╝░░░""")
        ascii_banner.setFont(QFont("Courier", 8))
        ascii_banner.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(ascii_banner)
        
        self.language_layout = QHBoxLayout()
        self.language_label = QLabel("Idioma/Language:")
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Español", "English"])
        self.language_combo.currentTextChanged.connect(self.cambiar_idioma)
        self.language_layout.addWidget(self.language_label)
        self.language_layout.addWidget(self.language_combo)
        self.layout.addLayout(self.language_layout)
        
        self.textos = {
            "Español": {
                "instrucciones_btn": "¿Cómo activar Depuración USB?",
                "estado_dispositivo": "Esperando conexión ADB...",
                "dispositivo_detectado": "Dispositivo ADB detectado.",
                "titulo_analisis": "¿Qué deseas analizar?",
                "checkbox_todos": "Todos los audios",
                "label_cantidad": "Cantidad de últimos audios:",
                "label_filtros": "Palabras clave adicionales (separadas por coma):",
                "placeholder_filtros": "Ej: visa, DNI, código",
                "analizar_btn": "Iniciar análisis",
                "placeholder_resultado": "Estado del proceso paso a paso...",
                "placeholder_salida": "Resultados encontrados...",
                "dispositivo_no_conectado": "Dispositivo no conectado",
                "mensaje_dispositivo": "Conecte un dispositivo Android con Depuración USB activada.",
                "iniciando_extraccion": "Iniciando extracción de audios...",
                "audios_copiados": "Audios copiados:",
                "analizando_whisper": "Analizando con Whisper...",
                "transcripcion_completada": "Transcripción completada.",
                "buscando_secretos": "Buscando secretos sensibles...",
                "secretos_encontrados": "Se encontraron {} posibles secretos.",
                "guardado_archivo": "Guardado en secretleak.txt",
                "analisis_configurado": "Análisis configurado:",
                "audios": "Audios:",
                "filtros": "Filtros:",
                "secretos_detectados": "Secretos detectados:",
                "no_secretos": "No se encontraron secretos sensibles en los audios analizados.",
                "todos": "Todos"
            },
            "English": {
                "instrucciones_btn": "How to enable USB Debugging?",
                "estado_dispositivo": "Waiting for ADB connection...",
                "dispositivo_detectado": "ADB device detected.",
                "titulo_analisis": "What do you want to analyze?",
                "checkbox_todos": "All audios",
                "label_cantidad": "Number of recent audios:",
                "label_filtros": "Additional keywords (comma separated):",
                "placeholder_filtros": "Ex: visa, ID, code",
                "analizar_btn": "Start analysis",
                "placeholder_resultado": "Step by step process status...",
                "placeholder_salida": "Found results...",
                "dispositivo_no_conectado": "Device not connected",
                "mensaje_dispositivo": "Connect an Android device with USB Debugging enabled.",
                "iniciando_extraccion": "Starting audio extraction...",
                "audios_copiados": "Audios copied:",
                "analizando_whisper": "Analyzing with Whisper...",
                "transcripcion_completada": "Transcription completed.",
                "buscando_secretos": "Searching for sensitive secrets...",
                "secretos_encontrados": "Found {} possible secrets.",
                "guardado_archivo": "Saved to secretleak.txt",
                "analisis_configurado": "Analysis configured:",
                "audios": "Audios:",
                "filtros": "Filters:",
                "secretos_detectados": "Detected secrets:",
                "no_secretos": "No sensitive secrets found in the analyzed audios.",
                "todos": "All"
            }
        }
        
        self.idioma_actual = "Español"

        self.instrucciones_btn = QPushButton(self.textos[self.idioma_actual]["instrucciones_btn"])
        self.instrucciones_btn.clicked.connect(self.mostrar_instrucciones)
        self.layout.addWidget(self.instrucciones_btn)

        self.estado_dispositivo = QLabel(self.textos[self.idioma_actual]["estado_dispositivo"])
        self.estado_dispositivo.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.estado_dispositivo)

        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_estado_adb)
        self.toggle = False
        self.timer.start(500)

        self.opciones_layout = QVBoxLayout()
        self.titulo_analisis = QLabel(self.textos[self.idioma_actual]["titulo_analisis"])
        self.opciones_layout.addWidget(self.titulo_analisis)

        self.checkbox_todos = QCheckBox(self.textos[self.idioma_actual]["checkbox_todos"])
        self.checkbox_todos.setChecked(True)
        self.checkbox_todos.stateChanged.connect(self.toggle_cantidad)
        self.opciones_layout.addWidget(self.checkbox_todos)

        self.hbox = QHBoxLayout()
        self.label_cantidad = QLabel(self.textos[self.idioma_actual]["label_cantidad"])
        self.label_cantidad.setEnabled(False)
        self.hbox.addWidget(self.label_cantidad)

        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setRange(1, 1000)
        self.spin_cantidad.setEnabled(False)
        self.hbox.addWidget(self.spin_cantidad)
        self.opciones_layout.addLayout(self.hbox)

        self.label_filtros = QLabel(self.textos[self.idioma_actual]["label_filtros"])
        self.opciones_layout.addWidget(self.label_filtros)

        self.input_filtros = QLineEdit()
        self.input_filtros.setPlaceholderText(self.textos[self.idioma_actual]["placeholder_filtros"])
        self.opciones_layout.addWidget(self.input_filtros)

        self.layout.addLayout(self.opciones_layout)

        self.analizar_btn = QPushButton(self.textos[self.idioma_actual]["analizar_btn"])
        self.analizar_btn.clicked.connect(self.iniciar_analisis)
        self.layout.addWidget(self.analizar_btn)

        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setStyleSheet("background-color: #111; color: white;")
        self.resultado.setPlaceholderText(self.textos[self.idioma_actual]["placeholder_resultado"])
        self.layout.addWidget(self.resultado)

        self.salida = QTextEdit()
        self.salida.setReadOnly(True)
        self.salida.setStyleSheet("background-color: #222; color: white;")
        self.salida.setPlaceholderText(self.textos[self.idioma_actual]["placeholder_salida"])
        self.layout.addWidget(self.salida)

        self.setLayout(self.layout)

        self.adb_detectado = False
        self.filtros_por_defecto = {
            "Español": ["tarjeta de credito", "contraseña", "clave", "usuario", "tarjeta", "correo", "acceso", "banco", "password"],
            "English": ["credit card", "password", "key", "user", "card", "email", "access", "bank", "contraseña"]
        }

    def toggle_cantidad(self):
        estado = not self.checkbox_todos.isChecked()
        self.label_cantidad.setEnabled(estado)
        self.spin_cantidad.setEnabled(estado)

    def cambiar_idioma(self, idioma):
        self.idioma_actual = idioma
        self.actualizar_textos()
        
    def actualizar_textos(self):
        self.instrucciones_btn.setText(self.textos[self.idioma_actual]["instrucciones_btn"])
        self.titulo_analisis.setText(self.textos[self.idioma_actual]["titulo_analisis"])
        self.checkbox_todos.setText(self.textos[self.idioma_actual]["checkbox_todos"])
        self.label_cantidad.setText(self.textos[self.idioma_actual]["label_cantidad"])
        self.label_filtros.setText(self.textos[self.idioma_actual]["label_filtros"])
        self.input_filtros.setPlaceholderText(self.textos[self.idioma_actual]["placeholder_filtros"])
        self.analizar_btn.setText(self.textos[self.idioma_actual]["analizar_btn"])
        self.resultado.setPlaceholderText(self.textos[self.idioma_actual]["placeholder_resultado"])
        self.salida.setPlaceholderText(self.textos[self.idioma_actual]["placeholder_salida"])
        if not self.adb_detectado:
            self.estado_dispositivo.setText(self.textos[self.idioma_actual]["estado_dispositivo"])
        else:
            self.estado_dispositivo.setText(self.textos[self.idioma_actual]["dispositivo_detectado"])
        
    def mostrar_instrucciones(self):
        if self.idioma_actual == "Español":
            texto = (
                "1. Ir a Configuración del celular.\n"
                "2. Entrar a 'Acerca del teléfono' y presionar 7 veces sobre 'Número de compilación'.\n"
                "3. Volver atrás y entrar a 'Opciones de desarrollador'.\n"
                "4. Activar 'Depuración USB'.\n"
            )
            titulo = "Cómo activar la Depuración USB"
        else:
            texto = (
                "1. Go to phone Settings.\n"
                "2. Enter 'About phone' and tap 7 times on 'Build number'.\n"
                "3. Go back and enter 'Developer options'.\n"
                "4. Enable 'USB Debugging'.\n"
            )
            titulo = "How to enable USB Debugging"
        QMessageBox.information(self, titulo, texto)

    def actualizar_estado_adb(self):
        result = os.popen("adb get-state").read().strip()
        if "device" in result:
            self.estado_dispositivo.setText(self.textos[self.idioma_actual]["dispositivo_detectado"])
            self.timer.stop()
            self.adb_detectado = True
        else:
            self.toggle = not self.toggle
            estado = self.textos[self.idioma_actual]["estado_dispositivo"] if self.toggle else ""
            self.estado_dispositivo.setText(estado)

    def iniciar_analisis(self):
        if not self.adb_detectado:
            QMessageBox.warning(self, self.textos[self.idioma_actual]["dispositivo_no_conectado"], self.textos[self.idioma_actual]["mensaje_dispositivo"])
            return

        self.resultado.clear()
        self.salida.clear()
        threading.Thread(target=self.proceso_analisis, daemon=True).start()

    def proceso_analisis(self):
        self.resultado.append(self.textos[self.idioma_actual]["iniciando_extraccion"])
        os.system("mkdir Audios >nul 2>&1")
        result = os.popen("adb shell find '/storage/emulated/0/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Voice Notes/' -type f -name '*.opus'").read()
        files = sorted([f.strip() for f in result.strip().split("\n") if f.strip()])
        if not self.checkbox_todos.isChecked():
            files = files[-self.spin_cantidad.value():]

        for f in files:
            nombre = os.path.basename(f)
            os.system(f'adb pull "{f}" "Audios/{nombre}" >nul 2>&1')
        self.resultado.append(f"{self.textos[self.idioma_actual]['audios_copiados']} {len(files)}")

        self.resultado.append(self.textos[self.idioma_actual]["analizando_whisper"])
        os.system("del audioleak.txt >nul 2>&1")
        import whisper
        model = whisper.load_model("base")
        with open("audioleak.txt", "w", encoding="utf-8") as out_file:
            for f in files:
                nombre = os.path.basename(f)
                path_local = f"Audios/{nombre}"
                result = model.transcribe(path_local, language="es")
                out_file.write(result["text"] + "\n")
        self.resultado.append(self.textos[self.idioma_actual]["transcripcion_completada"])

        self.resultado.append(self.textos[self.idioma_actual]["buscando_secretos"])
        user_keywords = [x.strip().lower() for x in self.input_filtros.text().split(",") if x.strip()]
        filtros = self.filtros_por_defecto[self.idioma_actual] + user_keywords
        encontrados = []
        with open("audioleak.txt", "r", encoding="utf-8") as f:
            for linea in f:
                texto = linea.strip().lower()
                if any(filtro in texto for filtro in filtros):
                    encontrados.append(linea.strip())

        self.resultado.append(self.textos[self.idioma_actual]["secretos_encontrados"].format(len(encontrados)))
        if encontrados:
            with open("secretleak.txt", "w", encoding="utf-8") as out:
                for l in encontrados:
                    out.write(l + "\n")
        self.resultado.append(self.textos[self.idioma_actual]["guardado_archivo"])

        resumen_filtros = ", ".join(filtros)
        cantidad = self.textos[self.idioma_actual]["todos"] if self.checkbox_todos.isChecked() else self.spin_cantidad.value()
        self.resultado.append(f"\n{self.textos[self.idioma_actual]['analisis_configurado']}\n- {self.textos[self.idioma_actual]['audios']} {cantidad}\n- {self.textos[self.idioma_actual]['filtros']} {resumen_filtros}")

        if encontrados:
            self.salida.append(self.textos[self.idioma_actual]["secretos_detectados"])
            for linea in encontrados:
                self.salida.append(f" - {linea}")
        else:
            self.salida.append(self.textos[self.idioma_actual]["no_secretos"])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = OpusAuditApp()
    ventana.show()
    sys.exit(app.exec_())