class Nodo:
    todos = []   # registro de todos los nodos existentes

    def __init__(self, info=None):
        self.info = info    # Campo INFO
        self.liga = None    # Campo LIGA (NIL = None)
        Nodo.todos.append(self)


# ---------- UTILIDADES ----------

def recorrido(P):
    """Genera los nodos desde P siguiendo LIGA (protegido contra ciclos)."""
    visitados = set()
    actual = P
    while actual is not None and id(actual) not in visitados:
        visitados.add(id(actual))
        yield actual
        actual = actual.liga


def entrantes(nodo):
    """Cuántos nodos apuntan a 'nodo'."""
    return sum(1 for n in Nodo.todos if n.liga is nodo)


def buscar_nodo(info):
    """Devuelve el primer nodo registrado con esa información (o None)."""
    for n in Nodo.todos:
        if n.info == info:
            return n
    return None


# ---------- CREACIÓN (Algoritmo 5.1) ----------

def leer_res():
    while True:
        r = input("¿Desea ingresar más nodos a la lista? Sí: 1, No: 0: ")
        if r in ("0", "1"):
            return int(r)
        print("Escriba 1 o 0.")


def crea_inicio():
    """Algoritmo 5.1: crea la lista agregando cada nodo al inicio."""
    Nodo.todos.clear()          # se descarta la estructura anterior
    P = Nodo()
    P.info = input("Ingrese el dato del nodo: ")
    P.liga = None

    res = leer_res()
    while res == 1:
        Q = Nodo()
        Q.info = input("Ingrese el dato del nodo: ")
        Q.liga = P
        P = Q
        res = leer_res()
    return P


# ---------- RECORRIDO ----------

def recorrer(P):
    """Recorre desde el inicio. Los nodos compartidos se marcan con *."""
    if P is None:
        print("La lista está vacía")
        return
    hay_compartido = False
    for n in recorrido(P):
        marca = ""
        if entrantes(n) > 1:
            marca = "*"
            hay_compartido = True
        print(f"{n.info}{marca}", end=" -> ")
    print("NIL")
    if hay_compartido:
        print("(* = nodo al que apuntan dos o más nodos)")


def mostrar_estructura():
    """Muestra TODOS los nodos y hacia dónde apunta cada uno."""
    if not Nodo.todos:
        print("No hay nodos")
        return
    print("Nodo  ->  Apunta a   (nodos que apuntan a él)")
    for n in Nodo.todos:
        destino = n.liga.info if n.liga else "NIL"
        print(f"{n.info}  ->  {destino}   ({entrantes(n)})")


# ---------- INSERCIÓN ----------

def insertar_inicio(P, dato):
    Q = Nodo(dato)
    Q.liga = P
    return Q


def insertar_final(P, dato):
    Q = Nodo(dato)
    if P is None:
        return Q
    ultimo = None
    for n in recorrido(P):
        ultimo = n
    ultimo.liga = Q
    return P


def insertar_antes(P, X, dato):
    if P is None:
        print("La lista está vacía")
        return P
    if P.info == X:
        return insertar_inicio(P, dato)

    for anterior in recorrido(P):
        if anterior.liga is not None and anterior.liga.info == X:
            Q = Nodo(dato)
            Q.liga = anterior.liga
            anterior.liga = Q
            return P
    print(f"El valor {X} no se encuentra en la lista")
    return P


def insertar_despues(P, X, dato):
    for actual in recorrido(P):
        if actual.info == X:
            Q = Nodo(dato)
            Q.liga = actual.liga
            actual.liga = Q
            return P
    print(f"El valor {X} no se encuentra en la lista (o la lista está vacía)")
    return P


# ---------- BORRADO ----------

def borrar(P, X):
    """Borra el primer nodo con info X y redirige todos los punteros hacia él."""
    objetivo = None
    for n in recorrido(P):
        if n.info == X:
            objetivo = n
            break
    if objetivo is None:
        print(f"El valor {X} no se encuentra en la lista")
        return P

    # Todo nodo que apuntaba al borrado pasa a apuntar a su siguiente
    for n in Nodo.todos:
        if n.liga is objetivo:
            n.liga = objetivo.liga
    if P is objetivo:
        P = objetivo.liga
    Nodo.todos.remove(objetivo)
    print(f"Nodo con valor {X} eliminado")
    return P


# ---------- BÚSQUEDA ----------

def buscar(P, X):
    """Devuelve la posición de X (1 = primer nodo) o 0 si no existe."""
    for pos, n in enumerate(recorrido(P), start=1):
        if n.info == X:
            return pos
    return 0


# ---------- DOS NODOS APUNTAN AL MISMO NODO ----------

def enlazar_mismo_nodo():
    """Hace que los nodos A y B apunten ambos al nodo destino Z."""
    a = buscar_nodo(input("Valor del primer nodo (A): "))
    b = buscar_nodo(input("Valor del segundo nodo (B): "))
    z = buscar_nodo(input("Valor del nodo destino (Z): "))

    if a is None or b is None or z is None:
        print("Alguno de los nodos no existe")
        return
    if a is b:
        print("A y B deben ser nodos distintos")
        return
    if z is a or z is b:
        print("El destino no puede ser A ni B")
        return

    # Evitar ciclos: desde Z no se debe poder llegar a A ni a B
    for n in recorrido(z):
        if n is a or n is b:
            print("No se puede: se formaría un ciclo")
            return

    a.liga = z
    b.liga = z
    print(f"Los nodos {a.info} y {b.info} ahora apuntan a {z.info}")
    print("Nota: los nodos que estaban después de A o B pueden quedar "
          "fuera del recorrido; use la opción 7 para verlos.")


# ---------- MENÚS ----------

def menu_insercion(inicio):
    print("\n--- INSERTAR ---")
    print("1. Al inicio")
    print("2. Al final")
    print("3. Antes de X")
    print("4. Después de X")
    print("0. Volver")
    op = input("Elija una opción: ")

    if op == "1":
        inicio = insertar_inicio(inicio, input("Dato a insertar: "))
    elif op == "2":
        inicio = insertar_final(inicio, input("Dato a insertar: "))
    elif op == "3":
        X = input("Valor de X (insertar antes de): ")
        inicio = insertar_antes(inicio, X, input("Dato a insertar: "))
    elif op == "4":
        X = input("Valor de X (insertar después de): ")
        inicio = insertar_despues(inicio, X, input("Dato a insertar: "))
    elif op != "0":
        print("Opción no válida")
    return inicio


def main():
    inicio = None

    while True:
        print("\n========== LISTA SIMPLEMENTE LIGADA ==========")
        print("1. Crear lista (Algoritmo 5.1)")
        print("2. Recorrido de la lista")
        print("3. Inserción de un elemento")
        print("4. Borrado de un elemento")
        print("5. Búsqueda de un elemento")
        print("6. Hacer que dos nodos apunten a un mismo nodo")
        print("7. Mostrar estructura completa")
        print("0. Salir")
        opcion = input("Elija una opción: ")

        if opcion == "1":
            if inicio is not None:
                conf = input("Ya existe una lista; se reemplazará. ¿Continuar? (s/n): ")
                if conf.lower() != "s":
                    continue
            inicio = crea_inicio()
            recorrer(inicio)

        elif opcion == "2":
            recorrer(inicio)

        elif opcion == "3":
            inicio = menu_insercion(inicio)
            recorrer(inicio)

        elif opcion == "4":
            inicio = borrar(inicio, input("Valor del nodo a borrar: "))
            recorrer(inicio)

        elif opcion == "5":
            X = input("Valor a buscar: ")
            pos = buscar(inicio, X)
            if pos:
                print(f"El valor {X} se encuentra en la posición {pos}")
            else:
                print(f"El valor {X} no se encuentra en la lista")

        elif opcion == "6":
            enlazar_mismo_nodo()
            mostrar_estructura()

        elif opcion == "7":
            mostrar_estructura()

        elif opcion == "0":
            print("Programa terminado")
            break

        else:
            print("Opción no válida")


if __name__ == "__main__":
    main()