"""A helper class"""

class Helper(object):
    @staticmethod
    def symmetrize_numpy_matrix(mat):
        """mat is a NumPy.matrix or .array. Copies the lower diagonal elements
           to the upper diagonal elements."""
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                mat[i, j] = mat[j, i]
        return mat

    @staticmethod
    def symmetrize_list_matrix(mat, shape):
        """[IO]  mat is a list of lists. Copies the lower diagonal elements
           to the upper diagonal elements."""
        for i in range(shape[0]):
            for j in range(shape[1]):
                mat[i][j] = mat[j][i]

    @staticmethod
    def nullify_diagonal(mat):
        """Replaces negative numbers on the diagonal by 0.0.
           
           Sometimes variances of latent variables that are locally unidentified
           have been left free. These variances can become negative, making it
           impossible to take the sqrt(). One solution provided here is to set these
           variances to zero."""
        if mat.shape[0] != mat.shape[1]:
            raise Exception('Only square matrices can have the diagonal examined.')
        for i in range(mat.shape[0]):
            if mat[i, i] < 1e-12:
                mat[i, i] = 0.0
                sys.stderr.write('Replaced one negative number on diagonal by 0.\n')

    @staticmethod
    def nrows_symm(n):
        """Calculate number of rows a symmetric matrix must have had if 
           len(vech(matrix)) equals n"""
        from math import sqrt
        return int((sqrt(8*n + 1) - 1) / 2)
