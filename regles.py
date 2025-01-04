def blockade(a, x, y):
    """Bloque les cases adjacentes dans toutes les directions depuis la case (x, y)."""
    joueur = a[x][y]

    # Directions : haut, bas, gauche, droite, et diagonales
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
    
    for dx, dy in directions:
        bloc = False
        i = 1
        while True:
            nx, ny = x + i * dx, y + i * dy
            # Vérification des limites pour éviter l'IndexError
            if nx < 0 or ny < 0 or nx >= len(a) or ny >= len(a[0]):
                break
            if a[nx][ny] == 0:
                break
            if a[nx][ny] == joueur:
                bloc = True
                break
            i += 1
        if bloc:
            for j in range(1, i):
                a[x + j * dx][y + j * dy] = joueur

    return a

