import sys
from PyQt6.QtCore import Qt, QRectF, QTimer
from PyQt6.QtGui import QBrush, QColor, QAction
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
    QToolBar,
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

        # Variables d'état 
        self.composantes_presentes = []
        self.etat_outil = 0 # 0: Main, 1: Curseur, 2: Suppression, 3: Connexion

        #Création widget central & layout
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)
        self.layout_central = QVBoxLayout(self.widget_central)

        # Création du layout horizontal (contenant canvas et barre_droite)
        self.conteneur_layout_horizontal = QWidget()
        self.layout_central.addWidget(self.conteneur_layout_horizontal)
        self.layout_horizontal = QHBoxLayout(self.conteneur_layout_horizontal)

        # Ajouter le Canvas
        self.canvas = Canvas(self)
        self.layout_horizontal.addWidget(self.canvas)

        # Ajouter la Barre de Composantes
        self.barre_droite = BarreComposante(self.layout_horizontal, self.canvas.scene_graphique, self)

        # Ajout de la Barre d'outils 
        self.barre_outils = QToolBar()
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.barre_outils)
        action_main = QAction("Main", self)
        self.barre_outils.addAction(action_main)
        action_main.triggered.connect(self.action_main)
        action_curseur = QAction("Curseur", self)
        self.barre_outils.addAction(action_curseur)
        action_curseur.triggered.connect(self.action_curseur)
        action_suppression = QAction("Suppression", self)
        self.barre_outils.addAction(action_suppression)
        action_connexion = QAction("Connexion", self)
        self.barre_outils.addAction(action_connexion)

        # Création du Timer 
        self.main_timer = QTimer()
        self.count = 0
        self.main_timer.timeout.connect(self.main_update_loop)
        self.main_timer.start(10) # 100 fois chaque seconde

    def main_update_loop(self):
        self.count += 1 
        if self.count % 1000 == 0:
            print("Nombre de secondes de fonctionnement: " + str(self.count / 100))

    def action_main(self):
        if self.etat_outil != 0:
            self.canvas.activer_mouvement_canvas()
            for i in range(len(self.composantes_presentes)):
                self.composantes_presentes[i].setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsMovable, False)
                self.composantes_presentes[i].setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsSelectable, False)
            self.etat_outil = 0
    
    def action_curseur(self):
        if self.etat_outil != 1:
            self.canvas.desactiver_mouvement_canvas()
            for i in range(len(self.composantes_presentes)):
                self.composantes_presentes[i].setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsMovable)
                self.composantes_presentes[i].setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsSelectable)
            self.etat_outil = 1


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
    def __init__(self, layout_parent, scene, fenetre_principale):
        super().__init__()
        self.scene = scene
        self.fenetre_principale = fenetre_principale
        self.layout_barre_droite = QVBoxLayout(self)
        layout_parent.addWidget(self)


class BarreComposante(BarreDroite):
    def __init__(self, layout_parent, scene, fenetre_principale):
        super().__init__(layout_parent, scene, fenetre_principale)
        bouton_source = QPushButton("Source")
        self.layout_barre_droite.addWidget(bouton_source)
        bouton_resistance = QPushButton("Résistance")
        self.layout_barre_droite.addWidget(bouton_resistance)
        bouton_resistance.clicked.connect(self.ajout_source)

    # Fonction d'ajout 
    def ajout_source(self):
        resistance = Resistance()
        self.scene.addItem(resistance)
        self.fenetre_principale.composantes_presentes.append(resistance)


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