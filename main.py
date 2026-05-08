import sys
from PyQt6.QtCore import Qt, QRectF, QTimer
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, 
    QGraphicsView, 
    QGraphicsScene, 
    QVBoxLayout, 
    QHBoxLayout, 
    QPushButton, 
    QGraphicsItemGroup, 
    QGraphicsRectItem, 
    QGraphicsEllipseItem,
)

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
        self.layout_central = QHBoxLayout(self.widget_central)

        # Ajouter le Canvas
        self.canvas = Canvas(self)
        self.layout_central.addWidget(self.canvas)

        # Ajouter la Barre de Composantes
        self.barre_droite = BarreComposante(self.layout_central, self.canvas.scene_graphique)

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
        self.scene_graphique = QGraphicsScene(QRectF(-1000, -1000, 2000, 2000))
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
    
class BarreDroite(QWidget):
    def __init__(self, layout_parent, scene):
        super().__init__()
        self.scene = scene
        self.layout_barre_droite = QVBoxLayout(self)
        layout_parent.addWidget(self)


class BarreComposante(BarreDroite):
    def __init__(self, layout_parent, scene):
        super().__init__(layout_parent, scene)
        bouton_source = QPushButton("Source")
        self.layout_barre_droite.addWidget(bouton_source)
        bouton_resistance = QPushButton("Résistance")
        self.layout_barre_droite.addWidget(bouton_resistance)
        bouton_resistance.clicked.connect(self.ajout_source)

    # Fonction d'ajout 
    def ajout_source(self):
        resistance = Resistance()
        self.scene.addItem(resistance)


class Composante(QGraphicsItemGroup):
    def __init__(self):
        super().__init__()
        self.setPos(0, 0)


class Resistance(Composante):
    def __init__(self):
        super().__init__()
        self.rectangle = QGraphicsRectItem(QRectF(0, 0, 100, 100))
        self.rectangle.setBrush(QColor(255, 0, 0))
        self.addToGroup(self.rectangle)
        

if __name__ == "__main__":
    main()