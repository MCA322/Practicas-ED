import pathlib
from typing import List
from itertools import product

Asignacion = List[bool]

class Formula:
    def __init__(self, izquierda, conectivo=None, derecha=None):
        conectivos = ['C', 'D', 'I', 'E', 'N', 'B']
        if (conectivo is None
                and not (isinstance(izquierda, int) and izquierda > -1)):
            raise TypeError("Las variables deben ser naturales")
        elif conectivo is not None:
            if not isinstance(izquierda, Formula):
                raise TypeError("Los conectivos deben aplicarse a fórmulas")
            elif (conectivo == 'N' and derecha is not None):
                raise TypeError("En la negación no debe existir fórmula derecha")
            elif (conectivo not in conectivos):
                raise ValueError("El conectivo es incorrecto")
            elif (conectivo != 'N' and not isinstance(derecha, Formula)):
                raise TypeError("Los conectivos deben aplicarse a fórmulas")
        self.izquierda = izquierda
        self.conectivo = conectivo
        self.derecha = derecha

    def __repr__(self):
        if self.conectivo is None:
            return f"x{self.izquierda}"
        elif self.conectivo == 'N':
            return f"(¬{self.izquierda.__repr__()})"
        else:
            operadores = {
                'C': '∧',
                'D': '∨',
                'I': '→',
                'E': '↔',
                'B': '↔'
            }
            return f"({self.izquierda.__repr__()} {operadores[self.conectivo]} {self.derecha.__repr__()})"

    def lista_variables(self):
        if self.conectivo is None:
            return [self.izquierda]
        elif self.conectivo == 'N':
            return self.izquierda.lista_variables()
        else:
            left_vars = self.izquierda.lista_variables()
            right_vars = self.derecha.lista_variables()
            result = []
            for var in left_vars + right_vars:
                if var not in result:
                    result.append(var)
            return sorted(result)

    def ultima_variable(self):


    def numero_conectivos(self):


    def _evalua_aux(self, asignacion: Asignacion, posiciones: List[int]):
        if self.conectivo is None:
            index = posiciones.index(self.izquierda)
            return asignacion[index]
        elif self.conectivo == 'N':
            return not self.izquierda._evalua_aux(asignacion, posiciones)
        else:
            left_val = self.izquierda._evalua_aux(asignacion, posiciones)
            right_val = self.derecha._evalua_aux(asignacion, posiciones)
            if self.conectivo == 'C':
                return left_val and right_val
            elif self.conectivo == 'D':
                return left_val or right_val
            elif self.conectivo == 'I':
                return (not left_val) or right_val
            elif self.conectivo in ['E', 'B']:
                return left_val == right_val

    def evalua(self, asignacion: Asignacion):


    def aplana(self):
        if self.conectivo is None:
            return [self.__repr__()]
        elif self.conectivo == 'N':
            return self.izquierda.aplana() + [self.__repr__()]
        else:
            return (self.izquierda.aplana() + 
                    self.derecha.aplana() + 
                    [self.__repr__()])

    def aplana_sin_variables(self):
        if self.conectivo is None:
            return []
        elif self.conectivo == 'N':
            sublist = self.izquierda.aplana_sin_variables()
            sublist.append(self.__repr__())
            return sublist
        else:
            left_list = self.izquierda.aplana_sin_variables()
            right_list = self.derecha.aplana_sin_variables()
            combined = left_list + right_list
            combined.append(self.__repr__())
            return combined
