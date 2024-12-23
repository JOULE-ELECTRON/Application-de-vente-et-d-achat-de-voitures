import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import clients

class Car:
    def __init__(self, marque, modele, description, prix, image_path):
        self.marque = marque
        self.modele = modele
        self.description = description
        self.prix = prix
        self.image_path = image_path
    
    def Sound(self):
        return self.marque
    