import sys

class Simplex:
    def __init__(self, c, A, b, signs, maximize=True, M=1e6):
        """
        c: list of objective coefficients
        A: list of constraint coefficient lists
        b: list of RHS values
        signs: list of strings: '<=', '>=', '='
        maximize: True for max, False for min
        M: big-M penalty
        """
        self.c = c[:] if maximize else [-ci for ci in c]
        self.A = [row[:] for row in A]
        self.b = b[:]
        self.signs = signs[:]
        self.maximize = True  # work in max form
        self.M = M
        self._build_tableau()

    def _build_tableau(self):
        n = len(self.c)
        m = len(self.A)
        # variable counts
        self.var_names = [f'x{i+1}' for i in range(n)]
        slack_idx = 0
        art_idx = 0
        # build initial rows
        rows = []
        art_vars = []
        for i in range(m):
            row = self.A[i][:]
            sign = self.signs[i]
            # slack/surplus/artificial
            if sign == '<=':
                row += [1]
                self.var_names.append(f's{slack_idx+1}')
                slack_idx += 1
                # no artificial
                for _ in range(m - slack_idx - art_idx): row.append(0)
            elif sign == '>=':
                # surplus
                row += [-1]
                self.var_names.append(f's{slack_idx+1}')
                slack_idx += 1
                # artificial
                row += [1]
                self.var_names.append(f'a{art_idx+1}')
                art_vars.append(n + slack_idx + art_idx)
                art_idx += 1
                for _ in range(m - slack_idx - art_idx): row.append(0)
            elif sign == '=':
                # no slack, add zero slack var
                row += [0] * slack_idx
                # artificial
                row += [1]
                self.var_names.append(f'a{art_idx+1}')
                art_vars.append(n + slack_idx + art_idx)
                art_idx += 1
                for _ in range(m - slack_idx - art_idx): row.append(0)
            else:
                raise ValueError(f"Invalid sign {sign}")
            row.append(self.b[i])
            rows.append(row)
        total_vars = len(self.var_names)
        # objective row: z - c x - M a = 0
        obj = [-ci for ci in self.c] + [0] * (total_vars - n)
        # subtract M for artificial
        for ai in art_vars:
            obj[ai] -= self.M
        obj.append(0)
        # assemble tableau
        self.tableau = rows + [obj]
        # track basic vars: slacks and artificials in each row
        self.basic = []
        for i in range(m):
            # slack is identity basis unless artificial
            for j in range(total_vars):
                if self.tableau[i][j] == 1 and sum(abs(self.tableau[k][j]) > 0 for k in range(m)) == 1:
                    self.basic.append(j)
                    break

    def _pivot(self, row, col):
        pivot = self.tableau[row][col]
        # normalize pivot row
        self.tableau[row] = [v / pivot for v in self.tableau[row]]
        # eliminate col in other rows
        for i in range(len(self.tableau)):
            if i != row:
                factor = self.tableau[i][col]
                self.tableau[i] = [self.tableau[i][j] - factor * self.tableau[row][j]
                                   for j in range(len(self.tableau[0]))]
        self.basic[row] = col

    def solve(self):
        m = len(self.A)
        ncols = len(self.tableau[0])
        # simplex iterations
        while True:
            # find entering var (most negative in objective)
            last = self.tableau[-1]
            enter = min((val, idx) for idx, val in enumerate(last[:-1]))
            if enter[0] >= 0:
                break  # optimal
            col = enter[1]
            # ratio test
            ratios = []
            for i in range(m):
                a = self.tableau[i][col]
                if a > 0:
                    ratios.append((self.tableau[i][-1] / a, i))
            if not ratios:
                raise ValueError("Unbounded solution")
            row = min(ratios)[1]
            self._pivot(row, col)
        # extract solution
        sol = [0] * len(self.var_names)
        for i, bi in enumerate(self.basic):
            sol[bi] = self.tableau[i][-1]
        obj = self.tableau[-1][-1]
        # if minimize, invert objective sign
        if not self.maximize:
            obj = -obj
        return {name: sol[i] for i, name in enumerate(self.var_names)}, obj

# Example usage
if __name__ == '__main__':
    # Maximize z = 3x1 + 5x2
    c = [3, 5]
    A = [[1, 1], [1, 0], [0, 1]]
    b = [4, 2, 3]
    signs = ['<=', '<=', '<=']
    solver = Simplex(c, A, b, signs, maximize=True)
    sol, val = solver.solve()
    print("Max solution:", sol, "Value:", val)

    # Minimize z = x1 + 2x2 subject to x1 + x2 >= 2, x1 >= 0, x2 >= 0
    c2 = [1, 2]
    A2 = [[1, 1]]
    b2 = [2]
    signs2 = ['>=']
    solver2 = Simplex(c2, A2, b2, signs2, maximize=False)
    sol2, val2 = solver2.solve()
    print("Min solution:", sol2, "Value:", val2)
