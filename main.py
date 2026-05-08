import sys
from PyQt6.QtCore import Qt, QRectF, QTimer
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsView, QGraphicsScene, QVBoxLayout

def main():
    app = QApplication(sys.argv)
    fenetre = FenetrePrincipale()
    fenetre.show()

    sys.exit(app.exec())

class FenetrePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PileAAA - Mini")

        #Création widget central & layout
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)
        self.layout_central = QVBoxLayout(self.widget_central)

        # Ajouter le Canvas
        self.canvas = Canvas(self)
        self.layout_central.addWidget(self.canvas)

        # Création du Timer 
        self.main_timer = QTimer()
        self.count = 0
        self.main_timer.timeout.connect(self.main_update_loop)
        self.main_timer.start(100) # 10 fois chaque seconde

    def main_update_loop(self):
        self.count += 1 
        if self.count % 100 == 0:
            print("Nombre de secondes de fonctionnement: " + str(self.count / 10))

class Canvas(QGraphicsView):
    def __init__(self, fenetre_principale):
        super().__init__()
        self.__fenetre_principale = fenetre_principale
        self.scene_graphique = QGraphicsScene(QRectF(0, 0, 2000, 2500))
        self.setScene(self.scene_graphique)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

    def get_fenetre_principale(self):
        return self.__fenetre_principale
    
    def activer_mouvement_canvas(self):
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        return "Mouvement du canvas activé"

    def desactiver_mouvement_canvas(self):
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        return "Mouvement du canvas désactivé"
        

if __name__ == "__main__":
    main()