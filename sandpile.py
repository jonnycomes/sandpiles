def topple(piles, row, col):
    height = len(piles)
    width = len(piles[0])
    pile = piles[row][col]
    if pile < 4:
        return piles
    piles[row][col] -= 4
    if row > 0:
        piles[row-1][col] += 1
    if row < height - 1:
        piles[row+1][col] += 1
    if col > 0:
        piles[row][col-1] += 1
    if col < width - 1:
        piles[row][col+1] += 1
    return piles

def complete_topple(piles):
    done = False
    while not done:
        done = True
        for row, row_pile in enumerate(piles):
            for col, cell in enumerate(row_pile):
                if cell > 3:
                    done = False
                    piles = topple(piles, row, col)
    return piles
